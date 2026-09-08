from collections.abc import Callable

from .request import HTTPRequest
from .response import HTTPResponse

Handler = Callable[[HTTPRequest], HTTPResponse]
Endpoint = Callable[[HTTPRequest], HTTPResponse]

class HTTPRouter:

    def __init__(self):
        self._routes: dict[tuple[str, str], Handler] = {}
        self._dynamic_handlers = {}

    def get_all(self) -> dict[tuple[str,str], Handler]:
        return self._routes

    def get(self, path: str, handler: Handler):
        self.register("GET", path, handler)

    def post(self, path: str, handler: Handler):
        self.register("POST", path, handler)

    def route(self, request: HTTPRequest) -> HTTPResponse | None:
        method = request.get_method()
        path = request.get_url().get_path()

        handler = self.resolve(method, path)
        if not handler:
            return None

        return handler(request)
    
    def endpoint(self, request: HTTPRequest) -> Endpoint:
        method = request.get_method()
        path = request.get_url().get_path()

        handler = self.resolve(method, path)
        
        def not_found_endpoint(_request: HTTPRequest) -> HTTPResponse:
            return HTTPResponse(
                status="404",
                reason_phrase="Not Found"
            )
        if not handler:
            return not_found_endpoint

        return handler
    
    def register(self, method: str, path: str, handler: Handler) -> None:
        self._routes[(method.upper(), path)] = handler

    def resolve(self, method: str, path: str) -> Handler | None:
        handler = self._routes.get((method.upper(), path))
        if handler:
            return handler