from urllib.parse import urlsplit, parse_qs

class URL:

    def __init__(self, path: str, query: dict[str, str], full_path: str):
        self._path = path
        self._query: dict[str, str] = query
        self._full_path = full_path

    @staticmethod
    def from_raw(raw: str):
        parsed = urlsplit(raw)

        query = {
            key: values[0]
            for key, values in parse_qs(parsed.query).items()
        }

        return URL(parsed.path, query, raw)
    
    def get_full_path(self) -> str:
        return self._full_path

    def get_path(self) -> str:
        return self._path

    def get_query(self) -> dict[str, str]:
        return self._query