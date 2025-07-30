# Logging model: 
from datetime import datetime 
from sqlmodel import Field, Session, SQLModel
from pydantic import field_validator
from config import DATE_FORMAT

class LogModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str 
    method: str 
    response: str 
    ip_address: str 
    start_time : datetime 
    end_time : datetime 
    time_elapsed : float 

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate(cls, dt: datetime) -> str:
        return dt.strftime(DATE_FORMAT)