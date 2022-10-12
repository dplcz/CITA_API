from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.main_models import *

from utils.async_util import db_session

indexRouter = APIRouter()


@indexRouter.get('/list-teacher')
async def get_teacher_list(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(select(TeacherModel))
    result = fetch_temp.fetchall()
    return result
