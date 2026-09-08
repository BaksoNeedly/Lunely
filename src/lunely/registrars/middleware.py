from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.middleware.pipeline import MiddlewarePipeline, NextHandler
from lunely.session.session import Session
from lunely.session.session_manager import SessionManager

class MiddlewareRegistrar:
    
    def __init__(self, pipeline: MiddlewarePipeline, session_manager: SessionManager) -> None:
        self._pipeline = pipeline
        self._session_manager = session_manager
    
    def register(self) -> None:
        self._pipeline.add(self.auth)
    
    def auth(self, request: HTTPRequest, next_handler: NextHandler) -> HTTPResponse:
        session = self._session_manager.extract_session(request)
        id = session.get_session_id() if session else self._session_manager.generate_id()
        if not session:
            session = Session(id)
            self._session_manager.set(session)
            return next_handler().set_cookie(
                "session_id",
                id
            )
        return next_handler()