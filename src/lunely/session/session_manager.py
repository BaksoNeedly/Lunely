import secrets
from ..session.session import Session
from ..http.request import HTTPRequest
from ..cookie.cookie import Cookie
from lunely.config import app_config

class SessionManager:

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def get_by_name(self, username: str) -> Session | None:
        for session_ in self.get_all().values():
            if session_.get_username().strip().lower() == username.strip().lower():
                return session_
        return None

    def get_all(self) -> dict[str, Session]:
        return self._sessions

    def set(self, session: Session) -> None:
        self._sessions[session.get_session_id()] = session

    def remove(self, session_id: str) -> Session | None:
        return self._sessions.pop(session_id, None)

    def contains(self, session_id: str) -> bool:
        return session_id in self._sessions

    def clear(self) -> None:
        self._sessions.clear()

    def size(self) -> int:
        return len(self._sessions)

    def generate_id(self) -> str:
        return secrets.token_urlsafe(32)
    
    def close(self, session_id: str) -> None:
        session = self.get(session_id)
        if session:
            user_socket = session.get_socket()
            if user_socket:
                user_socket.close()
            self.remove(session_id)


    def extract_session(self, request: HTTPRequest) -> Session | None:
        cookie = str(request.get_headers().get("cookie"))
        session_id = Cookie.parse(cookie.encode(app_config.ENCODING)).get("session_id")
        if not session_id:
            return None
        return self.get(str(session_id))
