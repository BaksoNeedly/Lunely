from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.http.router import HTTPRouter
from lunely.session.session import Session
from lunely.session.session_manager import SessionManager


class RouteRegistrar():
    
    def __init__(self, router: HTTPRouter):
        self._router = router
        
    def register(self) -> None:
        self._router.get("/", self.session_cookie)
    
    def session_cookie(self, request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        id = session.get_session_id() if session else SessionManager.generate_id()
        response = HTTPResponse()
        if not session:
            session = Session(id)
            response.set_cookie(
                "session_id",
                id
            )
        return response