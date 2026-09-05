from collections.abc import Callable

from ..utils.json_parser import JSONParser
from .frame import WebSocketFrame
from ..session.client_session import ClientSession
from .router_registry import WebSocketRouteRegistry


class WebSocketRouter:

    def __init__(self):
        self._handlers: dict[str, Callable] = {}
            
    def register(self, id: str, handler: Callable) -> None:
        self._handlers[id.strip().lower()] = handler
        
    def get(self, id: str) -> Callable | None:
        return self._handlers.get(id)

    def route(self, frame: bytes, client_session: ClientSession) -> None:
        raw_payload = WebSocketFrame.parse(frame)
        payload = JSONParser.parse(raw_payload)
        message_type = str(payload.get("type", "")).strip().lower()

        if not message_type:
            return

        handler = self.get(message_type)
        if handler is not None:
            handler(client_session, payload)
