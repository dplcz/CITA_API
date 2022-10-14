from sqlalchemy import BigInteger, Column, Float, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# print(__name__)

# 管理员数据表
class AdminModel(Base):
    __tablename__ = 'CITA_administrator'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_time = Column(DateTime, nullable=False)
    latest_login_time = Column(DateTime, nullable=False)


# 指导老师信息数据表
class TeacherModel(Base):
    __tablename__ = 'CITA_teacher'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    img_url = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    operation_time = Column(DateTime, nullable=False)
    operation_user = Column(Integer, ForeignKey('CITA_administrator.id'))


# 活动信息表
class ActivityModel(Base):
    __tablename__ = 'CITA_activity'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_title = Column(String(10), nullable=False)
    second_title = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    img_url = Column(String(255), nullable=False)
    resize_img_url = Column(String(255), nullable=False)
    detail_page_id = Column(Integer, nullable=False)
    detail_page_url = Column(String(255), nullable=True)
    operation_time = Column(DateTime, nullable=False)
    operation_user = Column(Integer, ForeignKey('CITA_administrator.id'))
