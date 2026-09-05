from collections.abc import Callable

class WebSocketRouteRegistry:
    
    def __init__(self):
        self._handlers: dict[str, Callable] = {}
        
    def register(self, id: str, handler: Callable) -> None:
        self._handlers[id.strip().lower()] = handler
        
    def get(self, id: str) -> Callable | None:
        return self._handlers.get(id)
