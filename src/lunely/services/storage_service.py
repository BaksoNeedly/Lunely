from pathlib import Path
from ..http.multipart import Multipart
from ..session.client_session import ClientSession
from lunely.config import app_config

class StorageService:

    STORAGE_PATH = Path(__file__).parent.parent.parent / "storage" / "private" / "user-files"

    @classmethod
    def save(cls, multipart: Multipart, path: str = None):
        filename = multipart.get_disposition().get(b"filename").decode(app_config.ENCODING).strip('"')
        if path is None:
            file_path = cls.STORAGE_PATH / filename
        else:
            file_path = Path(path) / filename

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(multipart.get_body())

    @classmethod
    def save_user_file(cls, client_session: ClientSession, multipart: Multipart):
        path = cls.STORAGE_PATH / str(client_session.get_serial_id())
        return cls.save(
            multipart,
            path
        )
