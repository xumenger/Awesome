##day-1搭建开发环境

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
