from lunely.config import app_config

class Cookie:

    @staticmethod
    def build(data: dict[str, str], path: str = "/", max_age: int = None, http_only: bool = True, same_site: str = "Lax"):
        response = ""
        for k, v in data.items():
            response += f"{k}={v}; "

        response += f"Path={path}; "
        if max_age is not None:
            response += f"Max-Age={max_age}; "
        response += f"HttpOnly; " if http_only else ""
        response += f"SameSite={same_site}; " if same_site else ""

        return response.rstrip("; ")

    @staticmethod
    def parse(cookie: bytes) -> dict[str, str]:
        for item in cookie.decode(app_config.ENCODING).split(";"):
            item = item.strip()

            if "=" not in item:
                continue

            key, value = item.split("=", 1)
            return {
                key: value
            }

        return {}
