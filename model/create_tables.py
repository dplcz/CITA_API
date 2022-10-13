from sqlalchemy import create_engine
from main_models import Base
from config.config import config

if __name__ == '__main__':
    # 创建数据表
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'], config['mysqldb']['sql_pass'],
                                                config['mysqldb']['sql_host'], config['mysqldb']['sql_port'],
                                                config['mysqldb']['database']), echo=True)

    Base.metadata.create_all(engine)
