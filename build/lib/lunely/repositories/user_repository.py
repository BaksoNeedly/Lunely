from ..database.database_manager import DatabaseManager
from ..models.user import User
from lunely.config import auth_tables
from ..utils.time_utils import TimeUtils


class UserRepository:
    """Database operations for chat_users."""

    @staticmethod
    def create(username: str, email: str, hash_password: str, is_verified: bool = False, verify_code: str | None = None, contacts: str = "[]") -> None:
        DatabaseManager.execute(
            f"INSERT INTO {auth_tables.USERS} "
            "(username, email, hash_password, is_verified, verify_code, contacts) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (username, email, hash_password, is_verified, verify_code, contacts),
        )

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        row = DatabaseManager.fetch_one(
            f"SELECT id, username, email, hash_password, is_verified, verify_code, contacts "
            f"FROM {auth_tables.USERS} WHERE id = %s",
            (user_id,), as_dict=True,
        )
        return UserRepository._to_user(row)

    @staticmethod
    def get_by_username(username: str) -> User | None:
        row = DatabaseManager.fetch_one(
            f"SELECT id, username, email, hash_password, is_verified, verify_code, contacts "
            f"FROM {auth_tables.USERS} WHERE username = %s",
            (username,), as_dict=True,
        )
        return UserRepository._to_user(row)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        row = DatabaseManager.fetch_one(
            f"SELECT id, username, email, hash_password, is_verified, verify_code, contacts "
            f"FROM {auth_tables.USERS} WHERE email = %s",
            (email,), as_dict=True,
        )
        return UserRepository._to_user(row)

    @staticmethod
    def get_by_verify_code(verify_code: str) -> User | None:
        row = DatabaseManager.fetch_one(
            f"SELECT id, username, email, hash_password, is_verified, verify_code, contacts "
            f"FROM {auth_tables.USERS} "
            "WHERE verify_code = %s AND is_verified IS FALSE",
            (verify_code,), as_dict=True,
        )
        return UserRepository._to_user(row)

    @staticmethod
    def get_all() -> list[User]:
        rows = DatabaseManager.fetch_all(
            f"SELECT id, username, email, is_verified, contacts "
            f"FROM {auth_tables.USERS} ORDER BY id",
            as_dict=True,
        )
        return [UserRepository._to_user(row) for row in rows]

    @staticmethod
    def mark_as_verified(user_id: int) -> None:
        DatabaseManager.execute(
            f"UPDATE {auth_tables.USERS} "
            "SET is_verified = TRUE, verify_code = NULL WHERE id = %s",
            (user_id,),
        )

    @staticmethod
    def update_verify_code(user_id: int, verify_code: str) -> None:
        DatabaseManager.execute(
            f"UPDATE {auth_tables.USERS} SET verify_code = %s WHERE id = %s",
            (verify_code, user_id),
        )

    @staticmethod
    def update_password(user_id: int, hash_password: str) -> None:
        DatabaseManager.execute(
            f"UPDATE {auth_tables.USERS} SET hash_password = %s WHERE id = %s",
            (hash_password, user_id),
        )

    @staticmethod
    def add_contact_to(to_user_id: int, add_contact: User, contacts_table: str) -> None:
        DatabaseManager.execute(
            f"""
            INSERT INTO {contacts_table}
                (user_id, contact_id, created_at)
            VALUES (%s, %s, %s)
            """,
            (to_user_id, add_contact.get_id(), TimeUtils.get_current_time_stamp()),
        )

    @staticmethod
    def update_contacts(user_id: int, contacts: str) -> None:
        DatabaseManager.execute(
            f"UPDATE {auth_tables.USERS} SET contacts = %s WHERE id = %s",
            (contacts, user_id),
        )

    @staticmethod
    def delete(user_id: int) -> None:
        DatabaseManager.execute(
            f"DELETE FROM {auth_tables.USERS} WHERE id = %s",
            (user_id,),
        )

    @staticmethod
    def _to_user(row: dict | None) -> User | None:
        if row is None:
            return None

        return User(
            user_id=row["id"],
            username=row["username"],
            email=row["email"],
            hash_password=row.get("hash_password"),
            is_verified=row.get("is_verified", False),
            verify_code=row.get("verify_code"),
        )
