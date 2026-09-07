from pathlib import Path
from lunely.http.request import HTTPRequest
from lunely.http.response import HTTPResponse
from lunely.http.server import HTTPServer
from lunely.packets.template import TemplatePacket
from lunely.session.client_session import ClientSession
from lunely.websocket.broadcaster import WebSocketBroadcaster


server = HTTPServer()
route = server.get_router()

path = Path(__file__).resolve().parent
frontend_path = path.parent / "frontend"
dist_path = frontend_path / "dist"

chat_path = frontend_path / "chat.html"
app_path = dist_path / "app.js"
header_path = dist_path / "header.js"
body_path = dist_path / "body.js"
footer_path = dist_path / "footer.js"

# It is important to add 'headers=...' to avoid undetected path.
def serve_chat(request: HTTPRequest) -> HTTPResponse:
    body = chat_path.read_text(encoding="utf-8")
    return HTTPResponse(body=body, headers={"Content-Type": "text/html; charset=utf-8"})

def serve_app(request: HTTPRequest) -> HTTPResponse:
    body = app_path.read_text(encoding="utf-8")
    return HTTPResponse(body=body, headers={"Content-Type": "text/javascript; charset=utf-8"})

def serve_header(request: HTTPRequest) -> HTTPResponse:
    body = header_path.read_text(encoding="utf-8")
    return HTTPResponse(body=body, headers={"Content-Type": "text/javascript; charset=utf-8"})

def serve_body(request: HTTPRequest) -> HTTPResponse:
    body = body_path.read_text(encoding="utf-8")
    return HTTPResponse(body=body, headers={"Content-Type": "text/javascript; charset=utf-8"})

def serve_footer(request: HTTPRequest) -> HTTPResponse:
    body = footer_path.read_text(encoding="utf-8")
    return HTTPResponse(body=body, headers={"Content-Type": "text/javascript; charset=utf-8"})

route.get("/", serve_chat)
route.get("/dist/app.js", serve_app)
route.get("/dist/header.js", serve_header)
route.get("/dist/body.js", serve_body)
route.get("/dist/footer.js", serve_footer)


websocket = server.get_websocket_server()
ws_route = websocket.get_router()

def send_message(client_session: ClientSession, payload: dict[str, str]) -> None:
    content = payload["content"]
    packet = TemplatePacket(
        type="message",
        data={
            "content": content
        }
    )
    WebSocketBroadcaster.send_to_all(packet, [client_session.get_session_id()])

def user_join(client_session: ClientSession, payload: dict[str, str]) -> None:
    packet = TemplatePacket(
        type="user_join_message",
        data={
            "username": "Anonymous"
        }
    )
    WebSocketBroadcaster.send_to_all(packet)
    
def user_join_message(client_session: ClientSession, payload: dict[str, str]) -> None:
    pass
    
    
def test(client_session: ClientSession, payload: dict[str, str]) -> None:
    print("test")
    
ws_route.register("user_join", user_join)
ws_route.register("message", send_message)
ws_route.register("test", test)
server.start() 