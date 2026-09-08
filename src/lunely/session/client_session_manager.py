from .client_session import ClientSession


class ClientSessionManager:
    def __init__(self) -> None:
        self._clients: dict[str, ClientSession] = {}

    def get(self, session_id: str) -> ClientSession | None: return self._clients.get(session_id)
    def get_by_name(self, username: str) -> ClientSession | None:
        return next((c for c in self._clients.values() if c.get_username() == username), None)
    def get_all(self) -> dict[str, ClientSession]: return self._clients
    def set(self, client: ClientSession) -> None: self._clients[client.get_session_id()] = client
    def remove(self, client: ClientSession) -> ClientSession | None: return self._clients.pop(client.get_session_id(), None)
    def contains(self, client: ClientSession) -> bool: return client.get_session_id() in self._clients
    def clear(self) -> None: self._clients.clear()
    def size(self) -> int: return len(self._clients)
    def close(self, client: ClientSession) -> None:
        if client:
            websocket = client.get_socket()
            if websocket: websocket.close()
            self.remove(client)
