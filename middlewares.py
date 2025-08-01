
from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.background import BackgroundTask
from models import LogModel


class LogggingMiddleware(BaseHTTPMiddleware):
    
    def add_to_db(self, model, session_local) -> None:
        session = session_local()
        session.add(model)
        session.commit()

    async def dispatch(self, request: Request, call_next) -> Response:

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

        background_task = BackgroundTask(self.add_to_db, log_obj, session_local)
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type, 
            background=background_task
        )