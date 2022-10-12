import uvicorn
from fastapi import FastAPI

import router.index_router
from config import config

from router.index_router import indexRouter

app = FastAPI()

app.include_router(indexRouter, prefix='/index', tags=['主页信息路由'])

if __name__ == '__main__':
    uvicorn.run(app, host="{}".format(config['web.conf'].get('ip_bind', '127.0.0.1')),
                port=int(config['web.conf'].get('port_bind', 8080)))
