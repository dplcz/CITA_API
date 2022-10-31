import enum

from fastapi import APIRouter, Depends, Form, Query, Response, Cookie
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from model.main_models import *

from utils.async_util import db_session
from utils.get_data_util import get_dict_result
from utils.token_util import judge_token, create_token

manageRouter = APIRouter(tags=['管理页面API接口路由'])

# 名称对应数据表
TYPE_LIST = {'teacher': TeacherModel, 'award': AwardModel, 'project': ProjectModel, 'activity': ActivityModel}


class ModelType(str, enum.Enum):
    teacher = 'teacher'
    award = 'award'
    project = 'project'
    activity = 'activity'


@manageRouter.post('/login')
async def login(token: str = Cookie(None), username: str = Form(None), password: str = Form(None),
                dbs: AsyncSession = Depends(db_session)):
    if token is not None:
        user = judge_token(token)
        if user is not None:
            response = Response(status_code=200)
            response.set_cookie('token', create_token(username), expires=3600, samesite='None')
            return response
        else:
            return Response(status_code=401, content='登录过期，请重新登录')
    elif username is not None and password is not None:
        fetch_temp = await dbs.execute(select(AdminModel.password).where(AdminModel.name == username))
        result = get_dict_result(data=fetch_temp)
        if len(result['data']) == 0:
            return Response(status_code=401, content='错误的密码或账户')
        else:

            if result['data'][0]['password'] == password:
                response = Response(status_code=200)
                response.set_cookie('token', create_token(username), expires=3600)
                return response
    else:
        return Response(status_code=400)


@manageRouter.get('/list/{select_type}')
async def list_activity(select_type: ModelType, token: str = Cookie(...), page: int = Query(1),
                        dbs: AsyncSession = Depends(db_session)):
    user = judge_token(token)
    if user is not None:
        data_model = TYPE_LIST[select_type]
        fetch_temp = await dbs.execute(
            select(data_model).slice((page - 1) * 10, page * 10))
        count_temp = await dbs.execute(count(data_model.id))
        result = get_dict_result(data=fetch_temp, count=count_temp, model=data_model.__name__)
        return result
    else:
        return Response(status_code=401, content='登录过期，请重新登录')
