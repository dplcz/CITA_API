from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.future import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ProgrammingError

from config import config

SQLALCHEMY_DATABASE_URL = 'mysql+aiomysql://{}:{}@{}:{}/{}'.format(config['mysqldb']['sql_user'],
                                                                   config['mysqldb']['sql_pass'],
                                                                   config['mysqldb']['sql_host'],
                                                                   config['mysqldb']['sql_port'],
                                                                   config['mysqldb']['database'])
# 创建异步连接引擎
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=False,
                             connect_args={'connect_timeout': 120}, pool_pre_ping=True)

async_session_local = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=True, bind=engine)


async def db_session() -> AsyncSession:
    async with async_session_local() as session:
        yield session
