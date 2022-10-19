import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import datetime

from config.config import config
from model.main_models import *

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'], config['mysqldb']['sql_pass'],
                                                config['mysqldb']['sql_host'], config['mysqldb']['sql_port'],
                                                config['mysqldb']['database']), echo=True)
    db_session = Session(engine)
    reader = csv.reader(open('../project_temp.csv', 'r', encoding='utf-8'))
    model_list = []
    header = next(reader)
    for i in reader:
        if len(i) > 0:
            temp_dict = {key: value for key, value in zip(header, i)}
            temp_dict['time'] = datetime.datetime.now()
            temp_dict['operation_time'] = datetime.datetime.now()
            temp_dict['operation_user'] = 1
            model_list.append(ProjectModel(**temp_dict))
    db_session.add_all(model_list)
    db_session.commit()
    db_session.close()