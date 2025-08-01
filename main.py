from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from sqlalchemy.orm import sessionmaker

from queries import average_task_duration
from middlewares import LogggingMiddleware
from db import orc_create_conn_pool, pg_create_engine



def create_db_and_tables(eng) -> None:
    SQLModel.metadata.create_all(eng)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.orc_connection = orc_create_conn_pool()
    app.state.engine = pg_create_engine()
    create_db_and_tables(app.state.engine)
    app.state.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=app.state.engine)
    yield
    


app = FastAPI(lifespan=lifespan)
app.add_middleware(LogggingMiddleware)



@app.get("/")
async def root() -> dict:
    return {'available_endpoints': ['/average_task_duration/employee_id=?']}




# Available endpoints
@app.get("/average_task_duration/employee_id={employee_id}")
async def get_average_task_duration(employee_id) -> list:
    async with app.state.orc_connection.acquire() as connection:
        with connection.cursor() as cursor:
            await cursor.execute(average_task_duration, emp_id=int(employee_id))
            formatted_result = await parse_query_result(cursor)
            return formatted_result
        











async def parse_query_result(cursor) -> list:
    column_names = [col.name.lower() for col in cursor.description]
    return [dict(zip(column_names, entry)) 
            async for entry in cursor]

