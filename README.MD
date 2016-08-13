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

**2016-08-05**

* 相关链接
  * http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013976160374750f95bd09087744569be5aae6160c8351000
  * https://github.com/michaelliao/awesome-python-webapp/blob/day-02/www/transwarp/db.py
* ! Python dict字典
  * http://www.cnblogs.com/waising/articles/2549116.html
  * http://www.cnblogs.com/waising/articles/2298254.html
* ! Python 面向对象
  * http://www.runoob.com/python/python-object.html
* ! Python 日志
  * logging线程安全的，可配置打印的格式
  * http://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html
* ! Python threadlocal
  * threadlocal提供了一个比thread模块更高层的API来提供线程的并发性
  * 这些线程并发运行并共享内存
  * http://blog.chinaunix.net/uid-27571599-id-3484048.html
  * http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832845200f6513494f0c64bd882f25818a0281e80000
* ! Python 装饰器
  * 装饰器可以对一个函数、方法或者类进行加工
  * http://www.cnblogs.com/vamei/archive/2013/02/16/2820212.html
* ! Python functools
  * http://blog.csdn.net/lwnylslwnyls/article/details/48007001
* ! Python time
  * http://www.runoob.com/python/att-time-time.html
* ! Python uuid
  * http://www.cnblogs.com/lijingchn/p/5299000.html
  * http://www.ietf.org/rfc/rfc4122.txt

**2016-08-13**

* ! Python 关键符号：\* and \*\*
  * http://blog.csdn.net/delphiwcdj/article/details/5746560
* ! Python dict tuple list set
  * https://liuzhichao.com/p/1645.html
  * 列表 [] 可以添加、删除元素 ['a', 'b', 'c']
  * 元组 () 和列表类似，但元组是不可变的 (1, 'a', 'b')
  * 集合 {} 无序不重复元素集，可新增、删除元素 {1, 2, 3, 4}
  * 字典 {} 键值对 {'a':123, 'b':'something'}