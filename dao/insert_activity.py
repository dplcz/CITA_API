from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime
from model.main_models import *
from config.config import config

# 测试插入活动数据

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'], config['mysqldb']['sql_pass'],
                                                config['mysqldb']['sql_host'], config['mysqldb']['sql_port'],
                                                config['mysqldb']['database']), echo=True)
    db_session = Session(engine)
    activity_mian = ActivityModel(first_title='招新面试', second_title='欢迎来到科技创新协会',
                                  time=datetime.datetime.strptime('2022-09-30', '%Y-%m-%d'),
                                  img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/activity_1.jpg',
                                  resize_img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/activity_1_resize.jpg',
                                  detail_page_id=1, operation_time=datetime.datetime.now(), operation_user=1)
    activity_bi = ActivityModel(first_title='招新笔试', second_title='欢迎来到科技创新协会',
                                time=datetime.datetime.strptime('2022-09-29', '%Y-%m-%d'),
                                img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/activity_2.jpg',
                                resize_img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/activity_2_resize.jpg',
                                detail_page_id=2, operation_time=datetime.datetime.now(), operation_user=1)
    db_session.add_all([activity_mian, activity_bi])
    db_session.commit()
    db_session.close()
