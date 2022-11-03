import enum
from typing import Optional

from fastapi import APIRouter, Depends, Form, Query, Response, Cookie, Header, Body
from sqlalchemy import select, desc, or_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from model.main_models import *

from utils.async_util import db_session
from utils.get_data_util import get_dict_result
from utils.token_util import judge_token, create_token

manageRouter = APIRouter(tags=['管理页面API接口路由'])

# 名称对应数据表
TYPE_DICT = {'teacher': TeacherModel, 'award': AwardModel, 'project': ProjectModel, 'activity': ActivityModel}
TYPE_LIST = [TeacherModel, AwardModel, ProjectModel, ActivityModel]


class ModelType(str, enum.Enum):
    teacher = 'teacher'
    award = 'award'
    project = 'project'
    activity = 'activity'


class DeleteType(str, enum.Enum):
    award = 'award'
    project = 'project'
    activity = 'activity'


@manageRouter.post('/login', tags=['实现登录和token更新接口'])
async def login(token: str = Cookie(None), origin: str = Header(...), username: str = Form(None),
                password: str = Form(None),
                dbs: AsyncSession = Depends(db_session)):
    """
    实现登录和token更新
    :param token: 用户验证
    :param origin: 来源网址
    :param username: 用户名
    :param password: 密码
    :param dbs: 异步数据库连接
    :return:
    """
    if username is not None and password is not None:
        fetch_temp = await dbs.execute(select(AdminModel.password, AdminModel.id).where(AdminModel.name == username))
        result = get_dict_result(data=fetch_temp)
        if len(result['data']) == 0:
            return Response(status_code=401, content='错误的密码或账户')
        else:

            if result['data'][0]['password'] == password:
                response = Response(status_code=200)
                response.init_headers({'Access-control-Allow-Origin': origin})
                response.set_cookie('token', create_token(username, result['data'][0]['id']), expires=3600,
                                    samesite=None)
                return response
            else:
                return Response(status_code=401)
    elif token is not None:
        judge_res = judge_token(token)
        if judge_res is not None:
            response = Response(status_code=200)
            response.init_headers({'Access-control-Allow-Origin': origin})
            response.set_cookie('token', create_token(judge_res['user'], judge_res['id']),
                                expires=3600,
                                samesite=None)
            return response
        else:
            return Response(status_code=401, content='登录过期，请重新登录')
    else:
        return Response(status_code=401)


@manageRouter.get('/list/{select_type}', tags=['通过接口名称查询模型数据'])
async def list_activity(select_type: ModelType, token: str = Cookie(...), page: int = Query(1),
                        dbs: AsyncSession = Depends(db_session)):
    """
    查询各种表的数据
    :param select_type: 查询类型
    :param token: 用户验证
    :param page: 分页查询
    :param dbs: 异步数据库连接
    :return:
    """
    judge_res = judge_token(token)
    if judge_res is not None:
        data_model = TYPE_DICT[select_type]
        fetch_temp = await dbs.execute(
            select(data_model).slice((page - 1) * 10, page * 10))
        count_temp = await dbs.execute(count(data_model.id))
        result = get_dict_result(data=fetch_temp, count=count_temp, model=data_model.__name__)
        return result
    else:
        return Response(status_code=401, content='登录过期，请重新登录')


@manageRouter.get('/search/{search_type}', tags=['通过接口名称模糊搜索数据'])
async def search_activity(search_type: ModelType, token: str = Cookie(...), page: int = Query(1),
                          query: str = Query(...),
                          dbs: AsyncSession = Depends(db_session)):
    """
    模糊搜索数据
    :param search_type: 搜索数据表
    :param token: 用户验证
    :param page: 分页查询
    :param query: 搜索字符
    :param dbs: 异步数据库连接
    :return:
    """

    judge_res = judge_token(token)
    if judge_res is not None:
        data_model = TYPE_DICT[search_type]
        word = '%{}%'.format(query)
        if data_model is ActivityModel:
            rule = or_(*[ActivityModel.first_title.like(word), ActivityModel.second_title.like(word),
                         ActivityModel.time.like(word)])

        elif data_model is ProjectModel:
            rule = or_(*[ProjectModel.project_name.like(word), ProjectModel.project_description.like(word),
                         ProjectModel.time.like(word), ProjectModel.participant.like(word)])

        elif data_model is AwardModel:
            rule = or_(
                *[AwardModel.game_name.like(word), AwardModel.player_name.like(word), AwardModel.game_time.like(word),
                  AwardModel.type.like(word), AwardModel.level.like(word)])
        elif data_model is TeacherModel:
            rule = or_(
                *[TeacherModel.name.like(word), TeacherModel.description.like(word), TeacherModel.position.like(word)])
        else:
            return Response(status_code=404, content='该模型表不支持查询')
        fetch_temp = await dbs.execute(select(data_model).slice((page - 1) * 10, page * 10).filter(rule))
        count_temp = await dbs.execute(select(count(data_model.id)).filter(rule))
        result = get_dict_result(data=fetch_temp, count=count_temp, model=data_model.__name__)
        return result

    else:
        return Response(status_code=401, content='登录过期，请重新登录')


@manageRouter.post('/insert/{insert_type}', tags=['通过接口插入数据'])
async def insert(insert_type: ModelType, token: str = Cookie(...), data: dict = Body(...),
                 dbs: AsyncSession = Depends(db_session)):
    """
    插入数据
    :param insert_type: 插入数据表
    :param token: 用户验证
    :param data: 数据
    :param dbs: 异步数据库连接
    :return:
    """
    judge_res = judge_token(token)
    if judge_res is not None:
        data_model = TYPE_DICT[insert_type]
        data['operation_user'] = judge_res['id']
        try:
            temp_model = data_model(**data)
            dbs.add(temp_model)
            await dbs.commit()
            return Response(status_code=201, content='success')
        except ValueError:
            return Response(status_code=404, content='字段错误！')
    else:
        return Response(status_code=401, content='登录过期，请重新登录')


@manageRouter.delete('/delete/{delete_type}', tags=['通过接口删除数据'])
async def delete_data(delete_type: DeleteType, token: str = Cookie(...), del_id: int = Query(...),
                      dbs: AsyncSession = Depends(db_session)):
    """
    删除数据
    :param delete_type: 删除数据表
    :param token: 用户验证
    :param del_id: id
    :param dbs: 异步数据库连接
    :return:
    """
    judge_res = judge_token(token)
    if judge_res is not None:
        delete_model = TYPE_DICT[delete_type]
        operation_user = judge_res['id']

        temp = await dbs.execute(delete(delete_model).where(delete_model.id == del_id))

        if temp.rowcount >= 1:
            await dbs.commit()
            return Response(status_code=200)
        else:
            return Response(status_code=404)

    else:
        return Response(status_code=401, content='登录过期，请重新登录')


@manageRouter.post('/update/{update_type}', tags=['通过接口修改数据'])
async def update_data(update_type: ModelType, token: str = Cookie(...), act_id: int = Query(...),
                      data: dict = Body(...),
                      dbs: AsyncSession = Depends(db_session)):
    """
    修改数据
    :param update_type:
    :param token:
    :param act_id:
    :param data:
    :param dbs:
    :return:
    """

    judge_res = judge_token(token)
    if judge_res is not None:
        update_model = TYPE_DICT[update_type]
        operation_user = judge_res['id']
        temp = await dbs.execute(update(update_model).where(update_model.id == act_id).values(data))
        if temp.rowcount >= 1:
            await dbs.commit()
            return Response(status_code=200)
        else:
            return Response(status_code=404)
    else:
        return Response(status_code=401, content='登录过期，请重新登录')
