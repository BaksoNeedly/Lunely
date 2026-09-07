from typing import Callable

from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse

Handler = Callable[[HTTPRequest], HTTPResponse]
Endpoint = Handler
NextHandler = Callable[[], HTTPResponse]
Middleware = Callable[[HTTPRequest, NextHandler], HTTPResponse]

class MiddlewarePipeline:
    
    def __init__(self) -> None:
        self._hooks: list[Middleware] = []
    
    def add(self, middleware: Middleware) -> Middleware:
        self._hooks.append(middleware)
        return middleware
    
    def handle(self, request: HTTPRequest, endpoint: Endpoint) -> HTTPResponse:
        i = 0
        def dispatch(index: int) -> HTTPResponse:
            if index >= len(self._hooks):
                return endpoint(request)
            current = self._hooks[index]
            def next_handler() -> HTTPResponse:
                return dispatch(index + 1);
            return current(request, next_handler)
        return dispatch(i)
    