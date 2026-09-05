import socket
from ..packets.packet import Packet
from lunely.config import app_config
from .frame import WebSocketFrame
from ..utils.json_parser import JSONParser
from ..session.client_session_manager import ClientSessionManager

class WebSocketBroadcaster:

    @staticmethod
    def send(client_socket: socket.socket, packet: Packet):
        json_bytes = JSONParser.stringify(
            packet.to_data()
        ).encode(app_config.ENCODING)
        frame = WebSocketFrame.build(json_bytes)
        client_socket.sendall(frame)

    @staticmethod
    def send_to_all(packet: Packet, excluding: list[str] | None = None):
        if excluding is None:
            excluding = []

        json_bytes = JSONParser.stringify(packet.to_data()).encode(app_config.ENCODING)
        frame = WebSocketFrame.build(json_bytes)
        for id, client_ in ClientSessionManager.get_all().items():
            if id in excluding:
                continue

            if not client_.get_session().is_authenticated():
                continue

            client_.get_socket().sendall(frame)
