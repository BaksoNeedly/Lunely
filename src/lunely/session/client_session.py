import socket

from ..session.session import Session
from ..database.database_manager import DatabaseManager
from lunely.config import auth_tables


class ClientSession:
    def __init__(self, client_socket: socket.socket, client_session: Session):
        self._client_socket = client_socket
        self._client_session = client_session
        self._serial_id = None
        self._current_room: str | None = None
        self.initialize()

    def initialize(self) -> None:
        db = DatabaseManager.get_connection()
        with db.cursor() as cur:
            cur.execute(f"SELECT id FROM {auth_tables.USERS} WHERE username = %s", (self.get_username(),))
            data = cur.fetchone()
        if data:
            self._serial_id = data[0]

    def to_data(self) -> dict:
        return {"username": self.get_username()}

    def get_socket(self) -> socket.socket: return self._client_socket
    def get_session(self) -> Session: return self._client_session
    def get_username(self) -> str: return self.get_session().get_username()
    def get_session_id(self) -> str: return self.get_session().get_session_id()

    def get_serial_id(self) -> int | None: return self._serial_id
    def get_current_room_id(self) -> str | None: return self._current_room
    def set_current_room_id(self, room_id: str | None) -> None: self._current_room = room_id
