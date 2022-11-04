# CITA API

### Background

为CITA官网提供动态数据接口，后期考虑使用Go语言改写

### Install
fastapi为异步web框架，使用sqlalchemy支持异步连接数据库
```
python >= 3.7

pip3 install -U cos-python-sdk-v5
pip3 install fastapi >= 0.75.0
pip3 install PyJWT >= 2.4.0
pip3 install sqlalchemy >= 1.4.39
# 数据库引擎
pip3 install aiomysql >= 0.1.1
# 服务器
pip3 install uvicorn >= 0.17.5
# linux系统下可安装
pip3 install gunicorn >= 20.1.0
```

### Usage
配置文件config/conf.ini
```
[web.conf]
# 绑定ip
ip_bind = 0.0.0.0
# 绑定端口
port_bind = 9801
# 生成token的key
SECRET_KEY = 'zmxjsl'


[upload.conf]
secret_id = 腾讯云COS secret_id
secret_key = 腾讯云COS secret_key
region = 腾讯云COSregion region
token = 腾讯云COS token
bucket = 腾讯云COS bucket

[mysqldb]
# 数据库ip
sql_host = 127.0.0.1
# 数据库端口
sql_port = 3306
# 数据库用户名
sql_user = root
# 数据库用户名密码
sql_pass = 123456
# 数据库名称
database = CITA
```
启动服务
```
# windows下和linux下
# 使用uvicorn
python3 main_app.py

# linux下
python3.7 -m gunicorn main_app:app -b 0.0.0.0:9801 -w 4 -k uvicorn.workers.UvicornH11Worker -D
```