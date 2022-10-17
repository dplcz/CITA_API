from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from model.main_models import *

from utils.async_util import db_session

indexRouter = APIRouter(tags=['主页API接口路由'])


def get_dict_result(fetch_res):
    try:
        result_temp = fetch_res.fetchall()
        result = {'code': 0, 'data': []}
        for i in result_temp:
            temp = dict(i)
            # temp.pop('_sa_instance_state')
            result['data'].append(temp)
        return result
    except Exception:
        return {'code': 1}


@indexRouter.get('/list-teacher')
async def get_teacher_list(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        select(TeacherModel.id, TeacherModel.name, TeacherModel.img_url, TeacherModel.position,
               TeacherModel.description))
    result = get_dict_result(fetch_temp)
    return result


@indexRouter.get('/latest-activity')
async def get_latest_activity(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        select(ActivityModel.first_title, ActivityModel.second_title, ActivityModel.img_url,
               ActivityModel.resize_img_url, ActivityModel.time,
               ActivityModel.detail_page_id, ActivityModel.detail_page_url).limit(3).order_by(
            desc(ActivityModel.time)))
    result = get_dict_result(fetch_temp)
    return result


@indexRouter.get('/get-award-count')
async def get_award_count(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        "select count(id) as count,type from CITA_award group by type;")
    result = get_dict_result(fetch_temp)
    return result
