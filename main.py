import os

from oracledb import create_pool_async, AsyncConnectionPool
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER = os.environ.get("USERNAME")
PSWD = os.environ.get("PASSWORD")


def create_conn_pool() -> AsyncConnectionPool:
    return create_pool_async(
                                user=USER,
                                password=PSWD,
                                host="localhost",
                                port=1521,
                                service_name="xepdb1" 
                        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.connection = create_conn_pool()
    yield



app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    async with app.state.connection.acquire() as connection:
        with connection.cursor() as cursor:
            await cursor.execute("select * from target.fact_activity")
            async for result in cursor:
                return {'result': result}

