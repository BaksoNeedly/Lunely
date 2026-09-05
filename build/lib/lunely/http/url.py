from urllib.parse import urlsplit, parse_qs

class URL:

    def __init__(self, path: str, query: dict):
        self._path = path
        self._query = query

    @staticmethod
    def from_raw(raw: str):
        parsed = urlsplit(raw)

        query = {
            key: values[0]
            for key, values in parse_qs(parsed.query).items()
        }

        return URL(parsed.path, query)

    def get_path(self) -> str:
        return self._path

    def get_query(self) -> dict:
        return self._query