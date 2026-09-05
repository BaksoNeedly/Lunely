from .client_session import ClientSession


class ClientSessionManager:
    _clients: dict[str, ClientSession] = {}

    @classmethod
    def get(cls, session_id: str) -> ClientSession | None: return cls._clients.get(session_id)
    @classmethod
    def get_by_name(cls, username: str) -> ClientSession | None:
        return next((c for c in cls._clients.values() if c.get_username() == username), None)
    @classmethod
    def get_all(cls) -> dict[str, ClientSession]: return cls._clients
    @classmethod
    def set(cls, client: ClientSession) -> None: cls._clients[client.get_session_id()] = client
    @classmethod
    def remove(cls, client: ClientSession) -> ClientSession | None: return cls._clients.pop(client.get_session_id(), None)
    @classmethod
    def contains(cls, client: ClientSession) -> bool: return client.get_session_id() in cls._clients
    @classmethod
    def clear(cls) -> None: cls._clients.clear()
    @classmethod
    def size(cls) -> int: return len(cls._clients)
    @classmethod
    def close(cls, client: ClientSession) -> None:
        if client:
            websocket = client.get_socket()
            if websocket: websocket.close()
            cls.remove(client)
