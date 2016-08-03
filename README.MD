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

**2016-08-04**

* Python装饰器
* Python面向对象的基础语法
* Python多线程
* 调试现有功能代码，添加详细注释

