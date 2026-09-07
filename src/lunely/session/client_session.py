import socket

from ..session.session import Session

class ClientSession:
    def __init__(self, client_socket: socket.socket, client_session: Session):
        self._client_socket = client_socket
        self._client_session = client_session
        self._serial_id = None
        self._current_room: str | None = None

    def get_socket(self) -> socket.socket: return self._client_socket
    def get_session(self) -> Session: return self._client_session
    def get_username(self) -> str: return self.get_session().get_username()
    def get_session_id(self) -> str: return self.get_session().get_session_id()

    def get_current_room_id(self) -> str | None: return self._current_room
    def set_current_room_id(self, room_id: str | None) -> None: self._current_room = room_id
