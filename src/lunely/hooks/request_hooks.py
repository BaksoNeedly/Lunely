from typing import Callable

from lunely.http.request import HTTPRequest

Handler = Callable[[HTTPRequest], None]

class RequestHooks:
    
    def __init__(self) -> None:
        self._hooks: list[Handler] = []
        
    def get_all(self) -> list[Handler]:
        return self._hooks
        
    def add(self, handler: Handler) -> Handler:
        self._hooks.append(handler)
        return handler