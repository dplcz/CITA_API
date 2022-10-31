from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from model.main_models import *

from utils.async_util import db_session
from utils.get_data_util import get_dict_result

indexRouter = APIRouter(tags=['主页API接口路由'])


@indexRouter.get('/list-teacher', tags=['获取所有老师信息'])
async def get_teacher_list(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        select(TeacherModel.id, TeacherModel.name, TeacherModel.img_url, TeacherModel.position,
               TeacherModel.description))
    result = get_dict_result(data=fetch_temp)
    return result


@indexRouter.get('/latest-activity', tags=['获取最近3个活动信息'])
async def get_latest_activity(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        select(ActivityModel.first_title, ActivityModel.second_title, ActivityModel.img_url,
               ActivityModel.resize_img_url, ActivityModel.time,
               ActivityModel.detail_page_id, ActivityModel.detail_page_url).limit(3).order_by(
            desc(ActivityModel.time)))
    result = get_dict_result(data=fetch_temp)
    return result


@indexRouter.get('/get-award-count', tags=['获取各类奖项数量'])
async def get_award_count(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        "select count(id) as count,type from CITA_award group by type;")
    result = get_dict_result(data=fetch_temp)
    return result


@indexRouter.get('/latest-project', tags=['获取最近5个项目'])
async def get_latest_project(dbs: AsyncSession = Depends(db_session)):
    fetch_temp = await dbs.execute(
        select(ProjectModel.project_name, ProjectModel.project_img_url, ProjectModel.project_url,
               ProjectModel.time).limit(5).order_by(desc(ProjectModel.time)))
    result = get_dict_result(data=fetch_temp)
    return result
