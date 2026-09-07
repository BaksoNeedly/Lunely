from lunely.config import app_config
import json

class JSONParser:

    @staticmethod
    def parse(raw_data: bytes) -> dict[str, str]:
        return json.loads(raw_data.decode(app_config.ENCODING))

    @staticmethod
    def stringify(data: dict[str, str]) -> str:
        return json.dumps(data)
