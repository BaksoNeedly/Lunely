class DynamicRoute:

    def __init__(
        self,
        route_id: int,
        path: str,
        route_key: str,
        created_at: int,
    ):
        self._id = route_id
        self._path = path
        self._route_key = route_key
        self._created_at = created_at

    def get_id(self) -> int:
        return self._id

    def get_path(self) -> str:
        return self._path

    def get_route_key(self) -> str:
        return self._route_key

    def get_created_at(self) -> int:
        return self._created_at

    def to_data(self) -> dict:
        return {
            "id": self._id,
            "path": self._path,
            "route_key": self._route_key,
            "created_at": self._created_at,
        }
