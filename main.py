import os
import json
from os.path import join, dirname
from uuid import uuid4
from dotenv import load_dotenv
from datetime import datetime
from oracledb import create_pool_async, AsyncConnectionPool
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import ValidationError

from models import LogModel
from queries import average_task_duration



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER = os.environ.get("USERNAME")
PSWD = os.environ.get("PASSWORD")


#TO DO TODAY: implement the log functionality and containerize the application



#The middleware will serialize the information of interest as an entry in a table from another database
# I will try experimenting with a SQLite database in order to have a three-services 

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

@app.middleware("http")
async def log_middleware(request: Request, call_next):

    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()
   

    response_body = b""    
    async for chunk in response.body_iterator:
        response_body += chunk

    log_obj = LogModel(
            id=str(uuid4()),
            url=request.url.path,
            method=request.method,
            response=response_body,
            ip_address=request.client.host,
            start_time=start_time,
            end_time=end_time,
            time_elapsed=(end_time - start_time).total_seconds()
        )

    # Define a background task that would write the model to a database
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

@app.get("/")
async def root() -> dict:
    return {'available_endpoints': ['/average_task_duration/employee_id=?']}




# Available endpoints

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

