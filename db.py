
import oracledb
from sqlmodel import create_engine
from sqlalchemy import Engine
from config import settings


def pg_create_engine() -> Engine:
    return create_engine(
        url=settings.POSTGRES_URL,
        echo=False,
        pool_size=20
    )


def orc_create_conn_pool() -> oracledb.AsyncConnectionPool:
    return oracledb.create_pool_async(
            user=settings.ORC_USERNAME,
            password=settings.ORC_PASSWORD,
            host="source_db",
            port=1521,
            service_name="xepdb1" 
        )
