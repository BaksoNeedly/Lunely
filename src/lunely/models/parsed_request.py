from typing import TypedDict

class ParsedRequest(TypedDict):
    method: str
    path: str
    version: str
    headers: dict[str, str]
    header_end: int
    body: bytes