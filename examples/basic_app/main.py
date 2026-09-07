from pathlib import Path

from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.http.server import HTTPServer

server = HTTPServer()
INDEX_PATH = Path(__file__).parent / "index.html"


def serve_index(request: HTTPRequest) -> HTTPResponse:
    body = INDEX_PATH.read_text(encoding="utf-8")
    return HTTPResponse(
        headers={"Content-Type": "text/html; charset=utf-8"},
        body=body,
    )

server.get_router().get("/", serve_index)
server.start()
