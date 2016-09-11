#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Database operation module. This module is independent with web module
'''

import time
import logging

import db

class Field(object):
    _count = 0

    def __init__(self, **kw):
        self.name = kw.get('name', None)                    #列名
        self._default = kw.get('default', None)             #列默认值
        self.primary_key = kw.get('primary_key', False)     #列是否为主键
        self.nullable = kw.get('nullable', False)           #列是否可为空
        self.updatable = kw.get('updatable', True)          #列是否可更新
        self.insertable = kw.get('insertable', True)        #列是否可插入
        self.ddl = kw.get('ddl', '')                        #列对应的数据类型
        self._order = Field._count
        Field._count = Field._count + 1

    @property
    def default(self):
        d = self._default
        return d() if callable(d) else d

    def __str__(self):
        s = ['<%s:%s,%s,default(%s),' % (self.__class__.__name__, self.name, self.ddl, self._default)]
        self.nullable and s.append('N')
        self.updatable and s.append('U')
        self.insertable and s.append('I')
        s.append('>')
        return ''.join(s)

#字符串型列
class StringField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'varchar(255)'
        super(StringField, self).__init__(**kw)

#整型列
class IntegerField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0
        if not 'ddl' in kw:
            kw['ddl'] = 'bigint'
        super(IntegerField, self).__init__(**kw)

#浮点型列
class FloatField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0.0
        if not 'ddl' in kw:
            kw['ddl'] = 'real'
        super(FloatField, self).__init__(**kw)

#布尔型列
class BooleanField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = False
        if not 'ddl' in kw:
            kw['ddl'] = 'bool'
        super(BooleanField, self).__init__(**kw)

#文本型列
class TextField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'text'
        super(TextField, self).__init__(**kw)

class BlobField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'blob'
        super(BlobField, self).__init__(**kw)

class VersionField(Field):
    def __init__(self, name=None):
        super(VersionField, self).__init__(name=name, default=0, ddl='bigint')


#set是可变的，有add()、remove()等方法，既然是可变的，所以它不存在哈希值
#frozenset是冻结的集合，不可变，存在哈希值，好处是它可以作为字典的key，也可以作为其他集合的元素，一旦被创建就不能改变
_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])


#根据表名、mapping生成对应的创建表的SQL
def _gen_sql(table_name, mappings):
    pk = None
    sql = ['--generating SQL for %s:' % table_name, 'create table `%s` (' % table_name]
    for f in sorted(mappings.values(), lambda x, y: cmp(x._order, y._order)):
        if not hasattr(f, 'ddl'):
            raise StandardError('no dll in field "%s".' % n)
        ddl = f.ddl
        nullable = f.nullable
        if f.primary_key:
            pk = f.name
        sql.append(nullable and '   `%s` %s,' % (f.name, ddl) or '  `%s` %s not null,' % (f.name, ddl))
    sql.append('    primary key(`%s`)' % pk)
    sql.append(');')
    return '\n'.join(sql)

class ModelMetaclass(type):
    '''
    Metaclass for model objects
    '''
    def __new__(cls, name, bases, attrs):
        #skip base model class
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        #store all subclasses info
        if not hasattr(cls, 'subclasses'):
            cls.subclasses = {}
        if not name in cls.subclasses:
            cls.subclasses[name] = name
        else:
            logging.warning('Redefine class: %s' % name)

        logging.info('Scan ORMapping %s...' % name)
        mappings = dict()
        primary_key = None
        for k,v in attrs.iteritems():
            if isinstance(v, Field):
                if not v.name:
                    v.name = k
                logging.info('Found mapping: %s => %s' % (k, v))
                #check duplicate primary key
                if v.primary_key:
                    if primary_key:
                        raise TypeError('Cannot define more than 1 primary key in class: %s' % name)
                    if v.updatable:
                        logging.warning('NOTE: change primary key to non-updatable.')
                        v.updatable = False
                    if nullable:
                        logging.warning('NOTE: change primary key to non-nullable.')
                        v.nullable = False
                    primary_key = v
                mappings[k] = k
        #check exists of primary key
        if not primary_key:
            raise TypeError('primary key not define in class: %s' % name)
        for k in mappings.iterkeys():
            attrs.pop(k)
        if not'__table__' in attrs:
            attrs['__table__'] = name.lower()
        attrs['__mappings__'] = mappings
        attrs['__primary_key__'] = primary_key
        attrs['__sql__'] = lambda self: _gen_sql(attrs['__table__', mappings])
        for trigger in _triggers:
            if not trigger in attrs:
                attrs[trigger] = None
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    '''
    Base class for ORM
    '''
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def get(cls, pk):
        '''
        Get by primary key
        '''
        d = db.select_one('select * from where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
        return cls(**d) if d else None

    @classmethod
    def find_first(cls, where, *args):
        d = db.select_one('select * from %s %s' % (cls.__table__, where), *args)
        return cls(**d) if d else None

    @classmethod
    def find_all(cls, *args):
        L = db.select('select * from `%s`' % cls.__table__)
        return [cls(**d) for d in L]

    @classmethod
    def find_by(cls, where, *args):
        L = db.select('select * from `%s` %s' % (cls.__table__, where), *args)
        return [cls(**d) for d in L]

    @classmethod
    def count_all(cls):
        return db.select_int('select count(`%s`) from `%s`' % (cls.__primary_key__.name, cls.__table__))

    @classmethod
    def count_by(cls, where, *args):
        return db.select_int('select count(`%s`) from `%s` `%s' % (cls.__primary_key__.name, cls.__table__, where), *args)

    def update(self):
        self.pre_update and self.pre_update()
        L = []
        args = []
        for k,v in self.__mappings__.iteritems():
            if v.updatable:
                if hasattr(self, k):
                    arg = getattr(self, k)
                else:
                    arg = v.default
                    setattr(self, k, arg)
                L.append('`%s`=?' % k)
                args.append(arg)
        pk = self.__primary_key__.name
        args.append(getattr(self, pk))
        db.update('update `%s` set %s where %s=?' % (self.__table__, ','.join(L), pk), *args)
        return self

    def delete(self):
        self.pre_delete and self.pre_delete()
        pk = self.__primary_key__.name
        args = (getattr(self, pk), )
        db.update('delete from `%s` where `%s`=?' % (self.__table__, pk), *args)
        return self

    def insert(self):
        self.pre_insert and pre_insert()
        params = {}
        for k,v in self.__mappings__.iteritems():
            if v.insertable:
                if not hasattr(self, k):
                    setattr(self, k, v.default)
                params[v.name] = getattr(self, k)
        db.insert('%s' % self.__table__, **params)
        return self

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    db.create_engine('root', 'root', 'awesome')
    db.update('drop table if exists user')
    db.update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()
