from sqlalchemy import create_engine
from main_models import Base
from config.config import config

if __name__ == '__main__':
    # 创建数据表
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['conf']['mysqldb']['user'], config['conf']['mysqldb']['pass'],
                                                config['conf']['mysqldb']['host'], config['conf']['mysqldb']['port'],
                                                config['conf']['mysqldb']['database']), echo=True)

    Base.metadata.create_all(engine)
