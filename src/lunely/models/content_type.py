from enum import Enum


class ContentType(Enum):
    
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    APPLICATION_JSON = "application/json"
    APPLICATION_JAVASCRIPT = "application/javascript"