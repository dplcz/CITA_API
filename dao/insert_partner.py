import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import datetime

from config.config import config
from model.main_models import *
import xlrd

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'], config['mysqldb']['sql_pass'],
                                                config['mysqldb']['sql_host'], config['mysqldb']['sql_port'],
                                                config['mysqldb']['database']), echo=True)
    db_session = Session(engine)
    wb = xlrd.open_workbook('../2022_partner (2).xlsx')
    sh = wb.sheet_by_name('temp_sheet')
    # print(dict(zip(sh.row_values(0), sh.row_values(1))))
    header = sh.row_values(0)
    header[2] = 'class_'
    model_list = []
    for i in range(1, sh.nrows):
        temp_value = sh.row_values(i)
        temp_value[0] = int(temp_value[0])
        temp_value[3] = str(int(temp_value[3]))
        try:
            temp_value[-3] = str(int(temp_value[-3]))
        except ValueError:
            temp_value[-3] = None
        temp_value[-1] = str(int(temp_value[-1]))
        temp_dict = dict(zip(header, temp_value))
        temp_dict['operation_user'] = 1
        temp_model = PartnerModel(**temp_dict)
        model_list.append(temp_model)
    db_session.add_all(model_list)
    db_session.commit()
    db_session.close()
