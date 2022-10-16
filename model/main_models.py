from sqlalchemy import BigInteger, Column, Float, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
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
    name = Column(String(255), nullable=False, comment='老师名称')
    position = Column(String(255), nullable=False, comment='老师职位')
    img_url = Column(String(255), nullable=False, comment='老师图片网址')
    description = Column(Text, nullable=False, comment='老师描述')
    operation_time = Column(DateTime, nullable=False, comment='操作时间')
    operation_user = Column(Integer, ForeignKey('CITA_administrator.id'), comment='操作管理员')


# 活动信息表
class ActivityModel(Base):
    __tablename__ = 'CITA_activity'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_title = Column(String(10), nullable=False, comment='大标题')
    second_title = Column(String(20), nullable=False, comment='小标题')
    time = Column(DateTime, nullable=False, comment='活动时间')
    img_url = Column(String(255), nullable=False, comment='活动图片地址')
    resize_img_url = Column(String(255), nullable=False, comment='重建大小图片地址')
    detail_page_id = Column(Integer, nullable=False, comment='详情页id')
    detail_page_url = Column(String(255), nullable=True, comment='比赛名称')
    operation_time = Column(DateTime, nullable=False, comment='操作时间')
    operation_user = Column(Integer, ForeignKey('CITA_administrator.id'), comment='操作管理员')


class AwardModel(Base):
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
