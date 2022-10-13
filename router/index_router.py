from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.main_models import *

from utils.async_util import db_session

indexRouter = APIRouter()


@indexRouter.get('/list-teacher')
async def get_teacher_list(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(select(TeacherModel))
    filed_name = TeacherModel.__name__
    result_temp = fetch_temp.fetchall()
    result = {'code': 0, 'data': []}
    for i in result_temp:
        temp = dict(i)[filed_name].__dict__
        temp.pop('_sa_instance_state')
        result['data'].append(temp)
    return result
