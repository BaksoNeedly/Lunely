from pathlib import Path

from lunely.http.request import HTTPRequest
from lunely.http.server import HTTPServer
from lunely.http.server import HTTPResponse

server = HTTPServer()

def serve_index(request: HTTPRequest) -> HTTPResponse:
    current_path = Path(__file__).parent
    print(current_path)
    body = None
    with open(current_path / "index.html", "r", encoding="utf-8") as file:
        body = file.read()
    return HTTPResponse(body=body)

server.get_router().get("/", serve_index)
server.start()