from datetime import datetime

from sqlalchemy import BigInteger, Column, Float, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

Base = declarative_base()


# print(__name__)

class MyBaseModel(object):
    operation_time = Column(DateTime, nullable=False, comment='操作时间', default=datetime.now())

    @declared_attr
    def operation_user(self):
        return Column(Integer, ForeignKey('CITA_administrator.id'), nullable=False, comment='操作管理员')


# 管理员数据表
class AdminModel(Base):
    __tablename__ = 'CITA_administrator'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_time = Column(DateTime, nullable=False)
    latest_login_time = Column(DateTime, nullable=False)


# 操作记录数据表
class OperationModel(Base, MyBaseModel):
    __tablename__ = 'CITA_operation'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    op_type = Column(Enum('insert', 'delete', 'update'), nullable=False, comment='操作类型')
    op_sql = Column(Text, nullable=False, comment='操作sql')
    op_value = Column(Text, nullable=True, comment='插入value')


# 指导老师信息数据表
class TeacherModel(Base, MyBaseModel):
    __tablename__ = 'CITA_teacher'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='老师名称')
    position = Column(String(255), nullable=False, comment='老师职位')
    img_url = Column(String(255), nullable=False, comment='老师图片网址')
    description = Column(Text, nullable=False, comment='老师描述')


# 活动信息表
class ActivityModel(Base, MyBaseModel):
    __tablename__ = 'CITA_activity'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, comment='序列号')
    first_title = Column(String(255), nullable=False, comment='大标题')
    second_title = Column(String(255), nullable=False, comment='小标题')
    time = Column(DateTime, nullable=False, comment='活动时间')
    img_url = Column(String(255), nullable=False, comment='活动图片地址')
    resize_img_url = Column(String(255), nullable=False, comment='重建大小图片地址')
    detail_page_id = Column(Integer, nullable=True, comment='详情页id')
    detail_page_url = Column(String(255), nullable=True, comment='详情页url')
    type = Column(Integer, nullable=False, default=0, comment='活动类型')

    keys = Column(String(255), nullable=True, comment='图片的key,用分号隔开')


# 获奖情况表
class AwardModel(Base, MyBaseModel):
    __tablename__ = 'CITA_award'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_name = Column(String(255), nullable=False, comment='比赛名称')
    game_time = Column(DateTime, nullable=False, comment='比赛时间')
    player_name = Column(String(255), nullable=False, comment='参加选手名称')

    type = Column(Enum('国家级', '省级', '校级', '院级'), nullable=False, comment='获奖类型')
    level = Column(Enum('金奖', '银奖', '铜奖', '特等奖', '一等奖', '二等奖', '三等奖', '优秀奖', '优秀名次'),
                   nullable=False, comment='获奖等级')
    if_proved = Column(Boolean, nullable=False, default=False, comment='是否有证明')
    proved_img_or_url = Column(String(255), nullable=True, comment='证明图片或文件')


# 项目记录表
class ProjectModel(Base, MyBaseModel):
    __tablename__ = 'CITA_project'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(255), nullable=False, comment='项目名称')
    project_img_url = Column(String(255), nullable=False, comment='项目图片url')
    project_url = Column(String(255), nullable=True, comment='项目部署地址，可为空')
    project_description = Column(Text, nullable=True, comment='项目描述，可为空')

    participant = Column(String(255), nullable=True, comment='参与者，可为空')
    time = Column(DateTime, nullable=False, comment='创建时间')

    keys = Column(String(255), nullable=True, comment='图片的key,用分号隔开')


# 人员信息表
class PartnerModel(Base, MyBaseModel):
    __tablename__ = 'CITA_partner'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), nullable=False, comment='学号')
    name = Column(String(50), nullable=False, comment='姓名')
    department = Column(Enum('项目部', '竞赛部', '宣传部', '组织部', '其他'), nullable=False, comment='部门')
    sex = Column(Enum('男', '女'), nullable=False, comment='性别')
    class_ = Column(String(50), name='class', nullable=False, comment='班级')
    phone = Column(String(20), nullable=True, comment='电话号码')
    position = Column(Enum('主席团', '部长团', '干事'), nullable=False, comment='职务', index=True)
    year = Column(Integer, nullable=False, comment='任期')
