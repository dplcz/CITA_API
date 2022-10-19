import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime
from model.main_models import *
from config.config import config

# 测试插入管理员数据

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'], config['mysqldb']['sql_pass'],
                                                config['mysqldb']['sql_host'], config['mysqldb']['sql_port'],
                                                config['mysqldb']['database']), echo=True)
    db_session = Session(engine)
    reader = csv.reader(open('../new_award_temp.csv', 'r', encoding='utf-8'))
    model_list = []
    header = next(reader)
    for i in reader:
        if len(i) > 0:
            temp_dict = {key: (value if value != 'True' else True) for key, value in zip(header, i)}
            model_list.append(AwardModel(**temp_dict))
    db_session.add_all(model_list)
    db_session.commit()
    db_session.close()
