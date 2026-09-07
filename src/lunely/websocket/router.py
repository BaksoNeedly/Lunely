from collections.abc import Callable

from ..utils.json_parser import JSONParser
from .frame import WebSocketFrame
from ..session.client_session import ClientSession

Handler = Callable[[ClientSession, dict[str, str]], None]

class WebSocketRouter:

    def __init__(self):
        self._handlers: dict[str, Handler] = {}
            
    def register(self, id: str, handler: Handler) -> None:
        self._handlers[id.strip().lower()] = handler
        
    def get(self, id: str) -> Handler | None:
        return self._handlers.get(id)

    def route(self, frame: bytes, client_session: ClientSession) -> None:
        raw_payload = WebSocketFrame.parse(frame)
        payload = JSONParser.parse(raw_payload)
        type = str(payload.get("type", "")).strip().lower()

        if not type:
            print("Invalid websocket payload type.")
            return

        handler = self.get(type)
        if handler is not None:
            handler(client_session, payload)
