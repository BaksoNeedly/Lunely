from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.http.router import HTTPRouter
from lunely.session.session import Session
from lunely.session.session_manager import SessionManager


class RouteRegistrar():
    
    def __init__(self, router: HTTPRouter, session_manager: SessionManager):
        self._router = router
        self._session_manager = session_manager
        
    def register(self) -> None:
        self._router.get("/", self.session_cookie)
    
    def session_cookie(self, request: HTTPRequest) -> HTTPResponse:
        session = self._session_manager.extract_session(request)
        id = session.get_session_id() if session else self._session_manager.generate_id()
        response = HTTPResponse()
        if not session:
            session = Session(id)
            self._session_manager.set(session)
            response.set_cookie(
                "session_id",
                id
            )
        return response