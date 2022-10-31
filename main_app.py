import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.config import config

from router.index_router import indexRouter
from router.manage_router import manageRouter

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

app.include_router(indexRouter, prefix='/index', tags=['主页信息路由'])
app.include_router(manageRouter, prefix='/man', tags=['管理页面路由'])

if __name__ == '__main__':
    uvicorn.run(app, host="{}".format(config['web.conf'].get('ip_bind', '127.0.0.1')),
                port=int(config['web.conf'].get('port_bind', 8080)))
