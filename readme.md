# CITA API

### Background

为CITA官网提供动态数据接口，后期考虑使用Go语言改写

### Install
fastapi为异步web框架，使用sqlalchemy支持异步连接数据库
```
python >= 3.7

# 使用腾讯云COS
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
配置文件config/conf.json
```
{
  "description": "配置文件",
  "version": "1.0.0",
  "author": "dplcz",
  "conf": {
    "web": {
      "ip": "0.0.0.0",
      "port": 9801,
      "SECRET_KEY": "asdsad"
    },
    "upload": {
      "type": "lsky",
      "cos": {
        "secret_id": "secret_id",
        "secret_key": "secret_key",
        "region": "region",
        "token": null,
        "bucket": "bucket"
      },
      "lsky": {
        "host": "http://host/api/v1/upload",
        "authorization": "111"
      }
    },
    "mysqldb": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "11111",
      "pass": "12345",
      "database": "CITA"
    }
  }
}
```
启动服务
```
# windows下和linux下
# 使用uvicorn
python3 main_app.py

# linux下
python3.7 -m gunicorn main_app:app -b 0.0.0.0:9801 -w 4 -k uvicorn.workers.UvicornH11Worker -D
```