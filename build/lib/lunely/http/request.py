from .parser import HTTPParser
from .url import URL
import socket

class HTTPRequest:

    def __init__(self, raw: bytes, client_socket: socket.socket):
        data = HTTPParser.parse_request(raw, client_socket)
        self._data = data
        self._method: str = data["method"]
        self._url = URL.from_raw(data["path"])

        self._version: str = data["version"]
        self._headers = data["headers"]
        self._headers_end = data["header_end"]
        self._body = data["body"]

    def get_data(self):
        return self._data

    def get_method(self) -> str:
        return self._method

    def get_url(self) -> URL:
        return self._url

    def get_version(self):
        return self._version

    def get_headers(self) -> dict:
        return self._headers

    def get_headers_end(self):
        return self._headers_end

    def get_body(self) -> bytes:
        return self._body
