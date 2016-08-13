#!/usr/bin/env python
# -*- coding: utf-8 -*-

# db.py
# 参考自《Day2-编写数据库模块》

import time, uuid, functools, threading, logging

# Dict Object:
class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'"% key)
    def __setattr__(self, key, value):
        self[key] = value

def next_id(t=None):
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

def _profiling(start, sql=''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING][DB] %s: %s' %(t, sql))
    else:
        logging.info('[PROFILING][DB] %s: %s' % [t, sql])

class DBError(Exception):
    pass

class MultiColumnsError(DBError):
    pass

class _LasyConnection(object):
    def __init__(self):
        self.connection = None
    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()
    def commit(self):
        self.connection.commit()
    def rollback(self):
        self.connection.rollback()
    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()
    
# 数据库引擎对象
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()

engine = None

# 持有数据库链接的上下文对象
# 由于_DbCtx继承自threading.local
# 它持有的数据库连接对于每个线程看到的都是不一样的
# 任何一个线程都无法访问到其他线程持有的数据库连接
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0
    def is_init(self):
        return not self.connection is None
    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0
    def cleanup(self):
        self.connection.cleanup()
        self.connection = None
    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()

def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, password=passwrd, database=database, host=host, port=port)
    defaults = dict(user_unicode=True, charset='utf-8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    # test connection...
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))

# 有了上面两个全局变量,可以继续实现数据库连接的上下文
# 目的是自动获取和释放连接
class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self
    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()
    # 定义了__enter__()和__exit__()的对象可以用于with语句
    # 确保任何情况下__exit__()方法可以被调用

def connection():
    return _ConnectionCtx()

# 将_ConnectionCtx的作用域作用到一个函数调用上
# Connection对象是存储在_DbCtx这个threadlocal对象的
# 因此,嵌套使用with_connection()没有问题
# _DbCtx永远检测当前是否已经存在Connection
# 如果存在，直接使用，否则，打开一个新的Connection
def with_connection(func):
    '''
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper

# 事务嵌套比Connection嵌套复杂一点
# 因为事务嵌套需要计数，每遇到一层嵌套就+1
# 离开一层嵌套就-1,最后到0时提交事务
class _TransactionCtx(object):
    def _enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        logging.info('begin transaction...' if _db_ctx.transactions == 1 else 'join current transaction...')
        return self
    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()
    def commit(self):
        global _db_ctx
        logging.info('commit transaction...')
        try:
            _db_ctx.connection.commit()
        except:
            logging.warning('commit failed. try rollback...')
            _db_ctx.connection.rollback()
            logging.warning('rollback ok.')
            raise
    def rollback(self):
        global _db_ctx
        logging.warning('rollback transaction...')
        _db_ctx.connection.rollback()
        logging.info('rollback ok.')

def transaction():
    return _TransactionCtx()

def with_transaction(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        _start = time.time()
        with _TransactionCtx():
            return func(*args, **kw)
        _profiling(_start)
    return _wrapper

def _select(sql, first, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, x) for x in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()

@with_connection
def select_one(sql, *args):
    return _select(sql, True, *args)

@with_connection
def select_int(sql, *args):
    d = _select(sql, True, *args)
    if len(d) != 1:
        raise MultiColumnsError('Exception only one cloumn.')
    return d.values()[0]

@with_connection
def select(sql, *args):
    return _select(sql, False, *args)

@with_connection
def _update(sql, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL:%s, ARGS:%s' %(sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_ctx.transactions == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()

def insert(table, **kw):
    cols, args = zip(**kw.iteritems())
    sql = 'insert into `%s` (%s)' % (table, ','.join(['`%s`' % clo for col in clos]), ','.join(['?' for i in range(len(cols))]))
    return _update(sql, *args)

def update(sql, *args):
    return _update(sql, *args)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('www-data', 'www-data', 'test')
    update('drop table if exists user')
    update('create table user(id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()
