import os

from oracledb import create_pool_async, AsyncConnectionPool
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from os.path import join, dirname
from dotenv import load_dotenv
from collections import defaultdict

from queries import average_task_duration



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
async def root() -> dict:
    # async with app.state.connection.acquire() as connection:
    #     with connection.cursor() as cursor:
    #         await cursor.execute("select * from target.fact_activity")
    #         return {'result' : await cursor.fetchall()}
    return {'message': 'Success'}


@app.get("/average_task_duration/employee_id={employee_id}")
async def get_average_task_duration(employee_id) -> list:
    async with app.state.connection.acquire() as connection:
        with connection.cursor() as cursor:
            await cursor.execute(average_task_duration, emp_id=int(employee_id))
            formatted_result = await parse_query_result(cursor)

            return formatted_result
            
            
        

async def parse_query_result(cursor) -> list:
    column_names = [col.name.lower() for col in cursor.description]

    return [dict(zip(column_names, entry)) 
            async for entry in cursor]

