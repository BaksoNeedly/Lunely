import secrets
from ..session.session import Session
from ..http.request import HTTPRequest
from ..cookie.cookie import Cookie
from lunely.config import app_config

class SessionManager:

    _sessions: dict[str, Session] = {}

    @classmethod
    def get(cls, session_id: str) -> Session | None:
        return cls._sessions.get(session_id)

    @classmethod
    def get_by_name(cls, username: str) -> Session | None:
        for _, session_ in cls.get_all().items():
            if session_.get_username().strip().lower() == username.strip().lower():
                return session_
        return None

    @classmethod
    def get_all(cls, ) -> dict[str, Session]:
        return cls._sessions

    @classmethod
    def set(cls, session: Session) -> None:
        cls._sessions[session.get_session_id()] = session

    @classmethod
    def remove(cls, session_id: str) -> Session | None:
        return cls._sessions.pop(session_id, None)

    @classmethod
    def contains(cls, session_id: str) -> bool:
        return session_id in cls._sessions

    @classmethod
    def clear(cls, ) -> None:
        cls._sessions.clear()

    @classmethod
    def size(cls, ) -> int:
        return len(cls._sessions)

    @classmethod
    def generate_id(cls, ) -> str:
        return secrets.token_urlsafe(32)
    
    @classmethod
    def close(cls, session_id: str) -> None:
        session = cls.get(session_id)
        if session:
            user_socket = session.get_socket()
            if user_socket:
                user_socket.close()
            cls.remove(session_id)


    @staticmethod
    def extract_session(request: HTTPRequest) -> Session | None:
        cookie = str(request.get_headers().get("cookie"))
        session_id = Cookie.parse(cookie.encode(app_config.ENCODING)).get("session_id")
        if not session_id:
            return None
        session = SessionManager.get(str(session_id))
        return session
