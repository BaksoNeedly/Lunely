from lunely.config import app_config, server_config
import socket

class HTTPParser:

    @staticmethod
    def parse_request(request: bytes, client_socket: socket.socket) -> dict:
        header_end = request.find(b"\r\n\r\n")
        header = request[:header_end]
        header_text = header.decode(app_config.ENCODING)
        lines = header_text.split("\r\n")
        
        request_line = lines[0].split(" ", 2)
        if len(request_line) == 3:
            method, path, version = request_line
        else:
            method = request_line[0] if request_line else "none"
            path = "none"
            version = "none"

        body = request[header_end + 4:]

        headers = {}
        for line in lines[1:]:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        content_length = headers.get("content-length")        
        while content_length and len(body) < int(content_length):
            body += client_socket.recv(server_config.BUFFER_SIZE)

        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
            "header_end": header_end,
            "body": body
        }

    # @staticmethod
    # def parse_body(cls, client_socket: socket.socket, request: bytes) -> dict:
    #     request_data = cls.parse_request(request)
    #     header_end = request_data["header_end"]
    #     body = request[header_end + 4:]
    #     content_length = int(request_data["headers"].get("content-length", 0))

    #     while len(body) < content_length:
    #         chunk = client_socket.recv(server_config.BUFFER_SIZE)
    #         if not chunk:
    #             break
    #         body += chunk

    #     request_data["body"] = body
    #     return request_data
