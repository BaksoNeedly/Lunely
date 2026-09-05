from __future__ import annotations

from .request import HTTPRequest

class Multipart:

    def __init__(
        self,
        delimiter: bytes,
        disposition: bytes,
        type: bytes,
        delimiter_closing: bytes,
        body: bytes
    ):
        self._delimiter = delimiter
        self._disposition = disposition
        self._type = type
        self._delimiter_closing = delimiter_closing
        self._body = body

    def get_delimiter(self) -> bytes:
        return self._delimiter

    def get_disposition(self) -> bytes:
        return self._disposition

    def get_type(self) -> bytes:
        return self._type

    def get_delimiter_closing(self) -> bytes:
        return self._delimiter_closing

    def get_body(self) -> bytes:
        return self._body

    @staticmethod
    def parse(request: HTTPRequest) -> Multipart:
        raw_multipart = request.get_body()
        raw_multipart = raw_multipart.replace(b"------", b"")
        # raw_multipart = raw_multipart.replace(b"--", b"")
        raw_multipart_parts = raw_multipart.split(b"\r\n")

        delimiter = raw_multipart_parts[0]

        disposition = raw_multipart_parts[1]
        disposition_headers = {}
        for _ in disposition.split(b";"):
            if b"=" in _:
                k, v = _.split(b"=")
                disposition_headers[k.lower().strip()] = v.strip().lower()
            else:
                disposition_headers[_.lower()] = None

        type = raw_multipart_parts[2].split(b":", 1)[1].strip()
        body = raw_multipart[raw_multipart.find(b"\r\n\r\n") + 4:raw_multipart.find(delimiter + b"--") - 2]
        return Multipart(
            delimiter,
            disposition_headers,
            type,
            delimiter + b"--",
            body
        )
