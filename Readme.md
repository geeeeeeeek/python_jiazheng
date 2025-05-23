
### 功能介绍

> 一直想做一款管理系统，看了很多优秀的开源项目但是发现没有合适的。于是利用空闲休息时间开始自己写了一套管理系统。现将部分源码开源，如需完整源码，可以联系客服微信购买：lengqin1024

整个平台包括前台和后台两个部分。

- 前台功能包括：首页、详情页、用户中心、家政入驻模块。
- 后台功能包括：总览、家政管理、分类管理、标签管理、评论管理、用户管理、运营管理、日志管理、系统信息模块。


### 效果演示

前台地址： https://jiazheng.gitapp.cn

后台地址： https://jiazheng.gitapp.cn/admin

后台管理帐号：

用户名：admin123
密码：admin123

### 代码结构

- server目录是后端代码
- web目录是前端代码

### 运行步骤

#### 后端运行步骤

(1) 安装python 3.8

(2) 安装依赖。进入server目录下，执行 pip install -r requirements.txt

(3) 安装mysql 5.7数据库，并创建数据库，创建SQL如下：
```
CREATE DATABASE IF NOT EXISTS python_jiazheng DEFAULT CHARSET utf8 COLLATE utf8_general_ci
```
(4) 恢复shop.sql数据。在mysql下依次执行如下命令：

```
mysql> use xxx;
mysql> source D:/xxx/xxx/xxx.sql;
```

(5) 启动django服务。在server目录下执行：
```
python manage.py runserver
```

#### 前端运行步骤

(1) 安装node 16.14

(2) 进入web目录下，安装依赖，执行:
```
npm install 
```
(3) 运行项目
```
npm run dev
```


 

### 开发文档

[点击进入](doc.md)


### 参考论文

[点击查看](doc/python_jiazheng.docx)

### 付费咨询

微信（lengqin1024）



