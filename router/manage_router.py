import enum
import re
from typing import Optional

from fastapi import APIRouter, Depends, Form, Query, Response, Cookie, Header, Body, UploadFile, File
from sqlalchemy import select, desc, or_, delete, update, literal_column, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from sqlalchemy.dialects import mysql

from model.main_models import *
from model.literal_model import literalquery

from utils.async_util import db_session
from utils.get_data_util import get_dict_result, get_query_sql
from utils.token_util import judge_token, create_token
from utils.upload_img_util import ImageUploader

from config.config import config

manageRouter = APIRouter(tags=['管理页面API接口路由'])

# 名称对应数据表
TYPE_DICT = {'teacher': TeacherModel, 'award': AwardModel, 'project': ProjectModel, 'activity': ActivityModel,
             'student': PartnerModel}
TYPE_LIST = [TeacherModel, AwardModel, ProjectModel, ActivityModel, PartnerModel]

SIZE_PATTERN = re.compile('(\d+)x(\d+)')

uploader = ImageUploader()


class ModelType(str, enum.Enum):
    teacher = 'teacher'
    award = 'award'
    project = 'project'
    activity = 'activity'
    student = 'student'


class DeleteType(str, enum.Enum):
    award = 'award'
    project = 'project'
    activity = 'activity'
    student = 'student'


class ImgType(str, enum.Enum):
    activity = 'activity'
    project = 'project'
    other = 'other'


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
            return Response(status_code=401, content='错误的密码或账户'.encode('utf-8'))
        else:

            if result['data'][0]['password'] == password:
                response = Response(status_code=200)
                response.init_headers({'Access-control-Allow-Origin': origin})
                response.set_cookie('token', create_token(username, result['data'][0]['id']), expires=3600,
                                    samesite=None)
                sql = update(AdminModel).where(result['data'][0]['id'] == AdminModel.id).values(
                    {'latest_login_time': datetime.now()})
                temp = await dbs.execute(sql)
                if temp.rowcount >= 1:
                    await dbs.commit()
                    return response
                else:
                    return Response(status_code=400)
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
            return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))
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
        if data_model != ActivityModel:
            fetch_temp = await dbs.execute(
                select(data_model).slice((page - 1) * 10, page * 10))
        else:
            fetch_temp = await dbs.execute(
                select(data_model).slice((page - 1) * 10, page * 10).order_by(desc(data_model.id)))
        count_temp = await dbs.execute(count(data_model.id))
        result = get_dict_result(data=fetch_temp, count=count_temp, model=data_model.__name__)
        return result
    else:
        return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))


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
        elif data_model is PartnerModel:
            rule = or_(
                *[PartnerModel.name.like(word), PartnerModel.department.like(word), PartnerModel.number.like(word),
                  PartnerModel.position.like(word), PartnerModel.phone.like(word), PartnerModel.year.like(word)])
        else:
            return Response(status_code=404, content='该模型表不支持查询'.encode('utf-8'))
        fetch_temp = await dbs.execute(select(data_model).slice((page - 1) * 10, page * 10).filter(rule))
        count_temp = await dbs.execute(select(count(data_model.id)).filter(rule))
        result = get_dict_result(data=fetch_temp, count=count_temp, model=data_model.__name__)
        return result

    else:
        return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))


@manageRouter.post('/insert/{insert_type}', tags=['通过接口插入数据'])
async def insert_data(insert_type: ModelType, token: str = Cookie(...), data: dict = Body(...),
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
        operation_user = judge_res['id']
        data['operation_user'] = operation_user
        data['operation_time'] = datetime.now()
        try:
            temp_model = data_model(**data)

            # 插入操作记录表

            query = insert(data_model).values(data)
            # sql = literalquery(query)

            op_model = OperationModel(
                **{'op_type': 'insert', 'op_sql': str(query), 'op_value': str(data), 'operation_user': operation_user})
            # dbs.add(temp_model)
            temp = await dbs.execute(query)
            if temp.rowcount >= 1:
                dbs.add(op_model)
                await dbs.commit()
                return Response(status_code=201, content='success')
            else:
                return Response(status_code=404, content='添加失败'.encode('utf-8'))
        except ValueError:
            return Response(status_code=404, content='字段错误！'.encode('utf-8'))
        except IntegrityError:
            return Response(status_code=404, content='主键重复！'.encode('utf-8'))
    else:
        return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))


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

        fetch_temp = await dbs.execute(select(delete_model.keys).where(delete_model.id == del_id))
        keys_result = get_dict_result(data=fetch_temp)
        if keys_result['data'][0]['keys'] is not None:
            if not uploader.delete_file(keys_result['data'][0]['keys'].split(';')):
                return Response(status_code=404)

        query = delete(delete_model).where(delete_model.id == del_id)

        # 插入操作记录表
        sql = literalquery(query)
        op_model = OperationModel(**{'op_type': 'delete', 'op_sql': sql, 'operation_user': operation_user})
        temp = await dbs.execute(query)

        if temp.rowcount >= 1:
            dbs.add(op_model)
            await dbs.commit()
            return Response(status_code=200)
        else:
            return Response(status_code=404)

    else:
        return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))


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

        data['operation_user'] = operation_user
        data['operation_time'] = datetime.now()
        # data = solve_sql_data(data)
        query = update(update_model).where(update_model.id == act_id).values(data)

        # sql = literalquery(query)
        op_model = OperationModel(
            **{'op_type': 'update', 'op_sql': str(query), 'op_value': str(data), 'operation_user': operation_user})
        temp = await dbs.execute(query)
        if temp.rowcount >= 1:
            dbs.add(op_model)
            await dbs.commit()
            return Response(status_code=200)
        else:
            return Response(status_code=404)
    else:
        return Response(status_code=401, content='登录过期，请重新登录'.encode('utf-8'))


@manageRouter.post('/upload-img/{upload_type}', tags=['上传图片'])
async def upload_img(upload_type: ImgType, token: str = Cookie(...), content_length: int = Header(..., lt=2_100_000),
                     file: UploadFile = File(...), act_id: int = Form(...), replace: bool = Form(False),
                     resize: str = Form(None), dbs: AsyncSession = Depends(db_session)):
    """
    上传图片
    :param upload_type: 图片分类
    :param token: 用户验证
    :param content_length: 文件大小
    :param file: 文件
    :param act_id: 活动id
    :param replace: 是否替换
    :param resize: 重置大小
    :param dbs: 异步数据库连接
    :return:
    """

    judge_res = judge_token(token)
    if judge_res is not None:
        if replace:
            operation_user = judge_res['id']

            upload_model = TYPE_DICT[upload_type]
            fetch_temp = await dbs.execute(select(upload_model).where(upload_model.id == act_id))
            temp_res = get_dict_result(data=fetch_temp, model=upload_model.__name__)
            if len(temp_res['data']) == 0:
                return Response(status_code=404)

        result = {}

        file_content = await file.read()
        file_type = file.content_type.split('/')[-1]
        keys = None
        if resize is not None and resize != 'null':
            try:
                width, height = re.findall(SIZE_PATTERN, resize)[0]
                width = int(width)
                height = int(height)
                resize_file_name = '{}_{}_resize.{}'.format(upload_type, act_id, file_type)
                res = uploader.resize_img(file_content, width, height, resize_file_name, file_type)
                if res:
                    if config['conf']['upload']['type'] == 'cos':
                        result['resize_url'] = 'https://{}.cos.{}.myqcloud.com/{}'.format(
                            config['conf']['upload']['cos']['bucket'],
                            config['conf']['upload']['cos']['region'],
                            resize_file_name)
                    elif config['conf']['upload']['type'] == 'lsky':
                        result['resize_url'] = res[0]
                        keys = '{};'.format(res[1])
                else:
                    return Response(status_code=400, content='resize上传失败'.encode('utf-8'))
            except (ValueError, IndexError):
                return Response(status_code=404, content='resize 格式错误'.encode('utf-8'))
        file_name = '{}_{}.{}'.format(upload_type, act_id, file_type)
        res = uploader.upload_file(file_content, file_name)
        if res:
            if config['conf']['upload']['type'] == 'cos':
                result['url'] = 'https://{}.cos.{}.myqcloud.com/{}'.format(config['conf']['upload']['cos']['bucket'],
                                                                           config['conf']['upload']['cos']['region'],
                                                                           file_name)
            elif config['conf']['upload']['type'] == 'lsky':
                result['url'] = res[0]
            if replace:
                keys = '{};'.format(res[1]) if keys is None else '{}{};'.format(keys, res[1])
                data = {'img_url': result.get('url'), 'resize_img_url': result.get('resize_url', None), 'keys': keys}
                query = update(upload_model).where(upload_model.id == act_id).values(data)
                op_model = OperationModel(
                    **{'op_type': 'update', 'op_sql': str(query), 'op_value': str(data),
                       'operation_user': operation_user})
                temp = await dbs.execute(query)
                if temp.rowcount >= 1:
                    dbs.add(op_model)
                    await dbs.commit()
                else:
                    return Response(status_code=400, content='上传失败'.encode('utf-8'))
            return result
        else:
            return Response(status_code=400, content='上传失败'.encode('utf-8'))
