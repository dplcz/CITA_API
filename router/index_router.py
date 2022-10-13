from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.main_models import *

from utils.async_util import db_session

indexRouter = APIRouter()


def get_dict_result(Model: object, fetch_res):
    try:
        filed_name = Model.__name__
        result_temp = fetch_res.fetchall()
        result = {'code': 0, 'data': []}
        for i in result_temp:
            temp = dict(i)[filed_name].__dict__
            temp.pop('_sa_instance_state')
            result['data'].append(temp)
        return result
    except Exception:
        return {'code': 1}


@indexRouter.get('/list-teacher')
async def get_teacher_list(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(select(TeacherModel))
    result = get_dict_result(TeacherModel, fetch_temp)
    return result


@indexRouter.get('/latest-activity')
async def get_latest_activity(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(select(ActivityModel).limit(5).order_by(ActivityModel.time))
    result = get_dict_result(ActivityModel, fetch_temp)
    return result
