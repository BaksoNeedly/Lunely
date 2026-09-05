from lunely.config import app_config

class HTTPResponse:

    def __init__(self, version: str = "HTTP/1.1", status: str="200", reason_phrase: str = "OK", headers: dict | None = None, body: str | None = None):
        self._version = version
        self._status = status
        self._reason_phrase = reason_phrase
        self._headers = headers or {}
        self._body = body or ""

        self._response = (
            f"{self._version} "
            f"{self._status} "
            f"{self._reason_phrase}\r\n"
        )        

    def add_headers(self, key: str, value: str) -> None:
        self._headers[key] = value

    def get_body(self) -> str:
        return self._body

    def set_body(self, body: str):
        self._body = body

    def get_response(self) -> str:
        return self.build().decode(app_config.ENCODING)

    def build(self) -> bytes:
        response = self._response.encode(app_config.ENCODING)
        
        for key, value in self._headers.items():
            response += f"{key}: {value}\r\n".encode(app_config.ENCODING)
        response += b"\r\n"
        
        if isinstance(self._body, str):
            response += self._body.encode(app_config.ENCODING)
        elif isinstance(self._body, bytes):
            response += self._body
        else:
            response += str(self._body).encode(app_config.ENCODING)
            
        return response
