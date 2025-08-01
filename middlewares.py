import random

from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.background import BackgroundTask
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from models import LogModel




def add_to_db(model, session_local):
    session = session_local()
    session.add(model)
    session.commit()
    return 


class LogggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        session_local = request.app.state.session_maker

        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        

        response_body = b""    
        async for chunk in response.body_iterator:
            response_body += chunk

        log_obj = LogModel(
                url=request.url.path,
                method=request.method,
                response=response_body,
                ip_address=request.client.host,
                start_time=start_time,
                end_time=end_time,
                time_elapsed=(end_time - start_time).total_seconds()
        )

        background_task = BackgroundTask(add_to_db, log_obj, session_local)
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type, 
            background=background_task
        )