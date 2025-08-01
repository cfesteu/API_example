
import os
import oracledb
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlmodel import Session, SQLModel, create_engine

from config import settings


def pg_create_engine():
    return create_engine(
        url=settings.POSTGRES_URL,
        echo=False,
        pool_size=20
    )


def orc_create_conn_pool() -> oracledb.AsyncConnectionPool:
    return oracledb.create_pool_async(
            user=settings.ORC_USERNAME,
            password=settings.ORC_PASSWORD,
            host="localhost",
            port=1521,
            service_name="xepdb1" 
        )
