import socket

class Session:

    def __init__(self, id: str, username: str = None, email: str = None, user_socket: socket.socket = None):
        self._session_id = id
        self._username = username
        self._email = email
        self._is_authenticated = False
        self._socket = user_socket

    def get_session_id(self) -> str:
        return self._session_id

    def get_username(self) -> str:
        return self._username

    def get_email(self) -> str:
        return self._email

    def set_username(self, username: str) -> None:
        self._username = username

    def set_email(self, email: str) -> None:
        self._email = email

    def get_socket(self) -> socket.socket:
        return self._socket

    def set_socket(self, user_socket: socket.socket) -> None:
        self._socket = user_socket

    def is_authenticated(self) -> bool:
        return self._is_authenticated

    def authenticate(self) -> None:
        self._is_authenticated = True

    def reset(self) -> None:
        self._is_authenticated = False
        self._username = None
        self._email = None
        self._socket = None