from typing import Self

from lunely.config import app_config
from lunely.cookie.cookie import Cookie
from lunely.models.content_type import ContentType
from lunely.models.same_site import SameSite

class HTTPResponse:

    def __init__(
        self, 
        version: str = "HTTP/1.1", 
        status: str="200", 
        reason_phrase: str = "OK", 
        headers: dict[str, str] | None = None, 
        body: str | None = None
    ):
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
    
    def set_version(self, version: str) -> Self:
        self._version = version
        return self
    
    def get_status(self) -> str:
        return self._status
    
    def set_status(self, status: str) -> Self:
        self._status = status
        return self
    
    def get_reason_phrase(self) -> str:
        return self._reason_phrase
    
    def set_reason_phrase(self, reason: str) -> Self:
        self._reason_phrase = reason
        return self
    
    def get_headers(self) -> dict[str, str]:
        return self._headers
    
    def set_header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self
    
    def set_content_type(
        self, 
        content_type: ContentType, 
        charset: str | None = "utf-8", 
        boundary: str | None = None
    ):
        value = content_type.value
        params: list[str] = []
        if charset:
            params.append(f"charset={charset}")
        if boundary:
            params.append(f"boundary={boundary}")
            
        if params:
            value += "; " + "; ".join(params)
            
        self.set_header("Content-Type", value)
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

    def set_body(self, body: str) -> Self:
        self._body = body
        return self

    def get_response(self) -> str:
        return self.build().decode(app_config.ENCODING)

    def build(self) -> bytes:
        response = self._response.encode(app_config.ENCODING)
        
        body = b""
                
        if self._body:
            body = self._body.encode(app_config.ENCODING)
        elif isinstance(self._body, bytes):
            body = self._body
        else:
            body = str(self._body).encode(app_config.ENCODING)        
        
        self.set_header("Content-Length", str(len(body)))
        
        for key, value in self._headers.items():
            response += f"{key}: {value}\r\n".encode(app_config.ENCODING)
        response += b"\r\n"
        
        response += body
        
        return response
    
    def is_not_found(self) -> bool:
        return self.get_status() == "404"
    
class HTTPResponseHeaders:
    pass
    
class JSONResponse(HTTPResponse):
    def __init__(
        self,
        version: str = "HTTP/1.1",
        status: str = "200", 
        reason_phrase: str = "OK", 
        headers: dict[str, str] | None = None,
        body: str | None = None
    ):
        super().__init__(version, status, reason_phrase, headers, body)
        
        self.set_content_type(
            ContentType.APPLICATION_JSON
        )
        
class InternalErrorResponse(HTTPResponse):
    def __init__(
        self,
        version: str = "HTTP/1.1",
        status: str = "500", 
        reason_phrase: str = "Internal Server Error", 
        headers: dict[str, str] | None = None,
        body: str | None = None
    ):
        super().__init__(version, status, reason_phrase, headers, body)
        
        if not body:    
            self.set_content_type(
                ContentType.TEXT_PLAIN
            )
            self.set_body("Internal Server Error")