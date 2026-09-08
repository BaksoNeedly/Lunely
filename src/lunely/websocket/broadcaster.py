import socket
from ..packets.packet import Packet
from lunely.config import app_config
from .frame import WebSocketFrame
from ..utils.json_parser import JSONParser
from ..session.client_session_manager import ClientSessionManager

class WebSocketBroadcaster:

    def __init__(self, client_sessions: ClientSessionManager):
        self._client_sessions = client_sessions

    def send(self, client_socket: socket.socket, packet: Packet):
        json_bytes = JSONParser.stringify(
            packet.to_data()
        ).encode(app_config.ENCODING)
        frame = WebSocketFrame.build(json_bytes)
        client_socket.sendall(frame)

    def send_to_all(self, packet: Packet, excluding: list[str] | None = None):
        if excluding is None:
            excluding = []

        json_bytes = JSONParser.stringify(packet.to_data()).encode(app_config.ENCODING)
        frame = WebSocketFrame.build(json_bytes)
        for id, client_ in self._client_sessions.get_all().items():
            if id in excluding:
                continue

            client_.get_socket().sendall(frame)
