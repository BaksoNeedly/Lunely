from typing import Self

from lunely.config import app_config
from lunely.cookie.cookie import Cookie
from lunely.models.same_site import SameSite

class HTTPResponse:

    def __init__(self, version: str = "HTTP/1.1", status: str="200", reason_phrase: str = "OK", headers: dict[str, str] | None = None, body: str | None = None):
        self._version = version
        self._status = status
        self._reason_phrase = reason_phrase
        self._headers: dict[str, str] = headers or {}
        self._body = body or ""

        self._response = (
            f"{self._version} "
            f"{self._status} "
            f"{self._reason_phrase}\r\n"
        )
        
    def get_version(self) -> str:
        return self._version
    
    def get_status(self) -> str:
        return self._status
    
    def get_reason_phrase(self) -> str:
        return self._reason_phrase
    
    def get_headers(self) -> dict[str, str]:
        return self._headers
    
    def set_header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self
    
    def set_cookie(
        self,
        name: str,
        value: str,
        path: str = "/",
        max_age: int = 0,
        http_only: bool = True,
        same_site: SameSite = SameSite.LAX
    ) -> Self:
        self.set_header(
            "Set-Cookie",
            Cookie.build(
                {
                    name: value
                },
                path=path,
                max_age=max_age if not 0 or not None else None,
                http_only=http_only,
                same_site=same_site
            )
        )
        return self

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
        
        if self._body:
            response += self._body.encode(app_config.ENCODING)
        elif isinstance(self._body, bytes):
            response += self._body
        else:
            response += str(self._body).encode(app_config.ENCODING)
            
        return response
    
    def is_not_found(self) -> bool:
        return self.get_status() == "404"