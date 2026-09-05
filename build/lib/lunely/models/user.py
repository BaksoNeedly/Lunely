class User:

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        hash_password: str | None = None,
        is_verified: bool = False,
        verify_code: str | None = None,
    ):
        self._id = user_id
        self._username = username
        self._email = email
        self._hash_password = hash_password
        self._is_verified = is_verified
        self._verify_code = verify_code

    def get_id(self) -> int:
        return self._id

    def get_username(self) -> str:
        return self._username

    def get_email(self) -> str:
        return self._email

    def get_hash_password(self) -> str | None:
        return self._hash_password

    def is_verified(self) -> bool:
        return self._is_verified

    def get_verify_code(self) -> str | None:
        return self._verify_code

    def to_data(self) -> dict:
        return {
            "username": self._username,
            # "email": self._email,
            # "is_verified": self._is_verified,
        }
