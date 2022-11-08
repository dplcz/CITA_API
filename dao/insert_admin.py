from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.main_models import *
from config.config import config

# 测试插入管理员数据

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['conf']['mysqldb']['user'], config['conf']['mysqldb']['pass'],
                                                config['conf']['mysqldb']['host'], config['conf']['mysqldb']['port'],
                                                config['conf']['mysqldb']['database']), echo=True)
    # session = sessionmaker(bind=engine)
    db_session = Session(engine)
    # db_session.add(AdminModel(name='admin', password='dplcz666', created_time=datetime.now(),
    #                           latest_login_time=datetime.now()))
    db_session.commit()
    db_session.close()
