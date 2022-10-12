from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import datetime
from model.main_models import *

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:dp20020620@mysql.dplcz.cn:3306/CITA', echo=True)

    db_session = Session(engine)
    teacher_sun = TeacherModel(name='孙威', position='阿里云大数据讲师、慧科集团高级讲师、互联网高级架构师',
                               description='掌握云原生开发、微服务架构设计、推荐系统工程实现。多年互联网公司就业经历，能够组织规划中大型分布式项目开发交付。有丰富的大数据和云计算等前沿技术的教学实施经验。',
                               img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/sun_resize.jpg',
                               operation_time=datetime.datetime.now(), operation_user=1)
    teacher_zhu = TeacherModel(name='朱珠', position='数据分析师',
                               description='深度掌握机器学习、深度学习基本算法的理论和实践。多年互联网公司就业经历，并担任数据分析数据挖掘等工作',
                               img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/zhu_resize.jpg',
                               operation_time=datetime.datetime.now(), operation_user=1)
    teacher_yuan = TeacherModel(name='苑进延', position='慧科集团高级讲师',
                                description='曾在一加科技、深圳瑞立视从事Java后端开发工作。后从事大数据和软件技术教学工作。在江汉大学、湖南科技学院、新余学院、江西软件职业技术大学授课并指导学生项目。参与过训练营、大赛辅导等各种教学活动。技术钻研能力强，善于沟通，乐于解决学生问题。',
                                img_url='https://hxm-1314321198.cos.ap-nanjing.myqcloud.com/yuan_resize.jpg',
                                operation_time=datetime.datetime.now(), operation_user=1)
    db_session.add_all([teacher_sun, teacher_zhu, teacher_yuan])
    db_session.commit()
    db_session.close()
