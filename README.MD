##说明

* 参考[《廖雪峰的实战练习项目》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001397616003925a3d157284cd24bc0952d6c4a7c9d8c55000)
* 好比学写作文，学的时候觉得简单，写的时候就无从下笔了
* 用Python实际写一个Web App才能更好的理解和掌握Python
* 实战目标是一个Blog网站，包含日志、用户和评论3大部分

##环境搭建

首先，确认系统安装的Python版本是2.7.x：

```
$ python --version
Python 2.7.12
```

参考[《搭建Python虚拟环境》](http://www.xumenger.com/python-environment-20160801/)

创建一个新的虚拟环境，并切换到虚拟环境：

```
$ virtualenv virenv
$ source virenv/bin/activate
```

前端模板引擎JinJa2安装：

```
$ pip install jinja2
```

安装MySQL驱动程序mysql-connector：

```
$ pip install mysql-connector
```

##项目结构

选择一个工作目录，然后，我们建立如下的目录结构：

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

##跟踪

**day2: 2016-08-05**

* [《Day 2 - 编写数据库模块》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013976160374750f95bd09087744569be5aae6160c8351000)
* Python dict字典
  * [《python dict 两种遍历方式的比较》](http://www.cnblogs.com/waising/articles/2549116.html)
  * [《Python dict》](http://www.cnblogs.com/waising/articles/2298254.html)
* Python 面向对象
  * [《Python 面向对象》](http://www.runoob.com/python/python-object.html)
* Python 日志
  * logging线程安全的，可配置打印的格式
  * [《python 的日志logging模块学习》](http://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html)
* Python threadlocal
  * threadlocal提供了一个比thread模块更高层的API来提供线程的并发性
  * 这些线程并发运行并共享内存
  * [《python中threading模块详解（一）》](http://blog.chinaunix.net/uid-27571599-id-3484048.html)
  * [《ThreadLocal》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832845200f6513494f0c64bd882f25818a0281e80000)
* Python 装饰器
  * 装饰器可以对一个函数、方法或者类进行加工
  * [《Python深入05 装饰器》](http://www.cnblogs.com/vamei/archive/2013/02/16/2820212.html)
* Python functools
  * [《 Python模块(functools) 》](http://blog.csdn.net/lwnylslwnyls/article/details/48007001)
* Python time
  * [《Python time time()方法》](http://www.runoob.com/python/att-time-time.html)
* Python uuid
  * [《Python_uuid 学习总结》](http://www.cnblogs.com/lijingchn/p/5299000.html)
  * [《A Universally Unique IDentifier (UUID) URN Namespace》](http://www.ietf.org/rfc/rfc4122.txt)

**day3: 2016-08-13**

* [《Day 3 - 编写ORM》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001402228705570c9506d546a3349c6b7d64135127672fe000)
* Python 关键符号：\* and \*\*
  * [《Python在函数中使用*和**接收元组和列表》](http://blog.csdn.net/delphiwcdj/article/details/5746560)
* Python 列表 元组 集合 字典
  * [《Python语法小结（三） 元组、列表、字典和集合》](https://liuzhichao.com/p/1645.html)
  * 列表list [] 可以添加、删除元素 ['a', 'b', 'c']
  * 元组tuple () 和列表类似，但元组是不可变的 (1, 'a', 'b')
  * 集合set {} 无序不重复元素集，可新增、删除元素 {1, 2, 3, 4}
  * 字典dict {} 键值对 {'a':123, 'b':'something'}

**day4: 2016-08-13**

* [《Day 4 - 编写Model》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001402307049906212b8a97f1df4587962539baa31d1fcd000)
* 如何发现错误以及报错排查策略
  * 编写好一个py之后，初步使用`import ...py`的方式，可发现一些语法错误
  * 假如执行`import ...py`报错
  * 则可以根据输出的Traceback (most recent call last):信息分析函数调用过程
  * 结合报错信息、代码上下文进行定位和排查错误
* 针对今天的开发进行测试
  * 到项目根目录执行`mysql -u root -p < schema.sql`，创建需要的数据库和表
  * 到www目录执行`python`-->`import test_db`即可执行测试程序
* 测试的预期的输出结果如下

```
>>> import test
WARNING:root:NOTE: change primary key to non-updatable.
WARNING:root:NOTE: change primary key to non-updatable.
WARNING:root:NOTE: change primary key to non-updatable.
new user id: 00147108558998799cd9922cc5e474fbb1077725e1ac554000
find user's name: Test
find user: None
```

**day5: 2016-08-15**

* [《Day 5 - 编写Web框架》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0014023080708565bc89d6ab886481fb25a16cdc3b773f0000)
* Python Web FrameWork
  * [《什么是Web框架？》](http://www.xumenger.com/web-framework-20160727/)
  * [《Web开发》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832648091917b035146084c43b05754ec9408dfaf000)
  * [《HTTP协议简介》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832653051fd44e44e4f9e4ed08f3e5a5ab550358d000)
  * [《HTML简介》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386833123019425a41845ca540a19c9080e8f930d7e1000)
  * [《WSGI接口》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832689740b04430a98f614b6da89da2157ea3efe2000)
  * [《使用Web框架》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832704232d6fb5df42dd34a7890fa6254351faac7000)
  * [《使用模板》](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832805619b3e68a9cf16c4d0398d8af8f6d50e740000)
  * [《》]()