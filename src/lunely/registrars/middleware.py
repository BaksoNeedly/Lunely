from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.middleware.pipeline import MiddlewarePipeline, NextHandler
from lunely.session.session import Session
from lunely.session.session_manager import SessionManager

class MiddlewareRegistrar:
    
    def __init__(self, pipeline: MiddlewarePipeline) -> None:
        self._pipeline = pipeline
    
    def register(self) -> None:
        self._pipeline.add(self.auth)
    
    def auth(self, request: HTTPRequest, next_handler: NextHandler) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        id = session.get_session_id() if session else SessionManager.generate_id()
        if not session:
            session = Session(id)
            SessionManager.set(session)
            return next_handler().set_cookie(
                "session_id",
                id
            )
        return next_handler()