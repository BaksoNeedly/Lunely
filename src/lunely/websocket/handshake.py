from ..http.request import HTTPRequest
from ..http.response import HTTPResponse
from lunely.config import app_config, websocket_config
import hashlib
import base64
import socket

class WebSocketHandshake:

    @staticmethod
    def perform(client_socket: socket.socket, request: HTTPRequest):
        key = str(request.get_headers().get("sec-websocket-key"))
        accept_key = base64.b64encode(
            hashlib.sha1(
                (key + websocket_config.WEBSOCKET_GUID).encode(app_config.ENCODING)
            ).digest()
        ).decode(app_config.ENCODING)
        response = HTTPResponse(status="101", reason_phrase="Switching Protocols", headers={
            "Upgrade": "websocket",
            "Connection": "upgrade",
            "Sec-WebSocket-Accept": accept_key
        })
        client_socket.sendall(response.build())
