##day1-搭建开发环境

确认系统的Python版本

```
$ python --version
Python 2.7.12
```

搭建虚拟环境，并切换到虚拟环境

```
$ virtualenv venv
$ source venv/bin/activate
```

安装模板引擎JinJa2

```
$ pip install jinja2
```

安装MySQL驱动程序

```
$ pip install mysql-connector-python-rf==2.1.3
```

项目结构

```
awesome-python-webapp/   <-- 根目录
|
+- backup/               <-- 备份目录
|
+- conf/                 <-- 配置文件
|
+- dist/                 <-- 打包目录
|
+- www/                  <-- Web目录，存放.py文件
|  |
|  +- static/            <-- 存放静态文件
|  |
|  +- templates/         <-- 存放模板文件
|
+- LICENSE               <-- 代码LICENSE
|
+- README.MD
```

##day2-编写数据库模块

在一个Web APP中，所有数据，包括用户信息、发布的日志、评论等，都存储在数据库中，我们选择MySQL作为数据库

Web APP中有很多地方都要访问数据库。访问数据库就需要创建数据库链接、游标对象，然后执行SQL语句，最后处理异常、清理资源。这些访问数据库的代码如果分散到各个函数中，势必无法维护，也不利于代码复用

此外，在一个Web App中，有多个用户会同时访问，系统以多线程或多进程模式来处理每个用户的请求。假设以多线程为例，每个线程在访问数据库时，都必须创建仅属于自身的链接，对别的线程不可见，否则就会造成数据库混乱

所以，我们还要创建一个简单可靠的数据库访问模型，在一个线程中，能既安全又简单的操作数据库

为什么不选择SQLAlchemy？因为它太过庞大，过度地面向对象设计导致API 太复杂。所以决定自己设计一个封装基本select、insert、update和delete操作的DB模块:transwarp.db

>设计底层模块的原则是，根据上层调用者设计简单医用的API 接口，然后实现模块内部代码，而不是先实现内部代码，再考虑将什么样的接口暴露给用户！

在MySQL中创建测试用的数据库

```
perfect@perfect:~$ mysql -u root -proot
mysql> create database awesome;
```

进行简单测试，在命令行输入以下命令：

```
perfect@perfect:~$ python db.py
```

不出意外的话，去MySQL 的awesome 数据库中检查会有一张新增的user 表

关于数据库模块的更详细的介绍，参见[《Day 2 - 编写数据库模块》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013976160374750f95bd09087744569be5aae6160c8351000)

另外关于Python装饰器、functools，继续学习[《装饰器》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386819879946007bbf6ad052463ab18034f0254bf355000)
