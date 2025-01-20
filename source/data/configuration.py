from os import getenv

from dotenv import load_dotenv

class DotEnvVariableNotFound(Exception):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self):
        return f"Variable {self.variable_name} not found in .env file"


class Configuration:
    def __init__(self):
        load_dotenv()
        self._bot_token: str = self._get_bot_token()
        self._totp_secret: str = self._get_totp_secret()
        self._admins_ids: list[int] = self._get_admins_ids()
        self._database_connection_parameters: dict[
            str, str
        ] = self._get_database_connection_parameters()

    def _get_bot_token(self) -> str:
        bot_token = getenv("TG_BOT_TOKEN")
        if not bot_token:
            raise DotEnvVariableNotFound("TG_BOT_TOKEN")
        return bot_token

    def _get_totp_secret(self) -> str:
        totp_secret = getenv("TOTP_SECRET")
        if not totp_secret:
            raise DotEnvVariableNotFound("TOTP_SECRET")
        return totp_secret

    def _get_admins_ids(self) -> list[int]:
        admins_ids = getenv("ADMINS_IDS")
        if not admins_ids:
            raise DotEnvVariableNotFound("ADMINS_IDS")
        return [int(admin_id) for admin_id in admins_ids.split(",") if admin_id]

    def _get_database_connection_parameters(self) -> dict[str, str]:
        for parameter in [
            "DB_HOST",
            "DB_PORT",
            "DB_USER",
            "DB_USER_PASSWORD",
            "DB_NAME",
        ]:
            if not getenv(parameter):
                raise DotEnvVariableNotFound(parameter)

        return {
            "host": getenv("DB_HOST"),
            "port": getenv("DB_PORT"),
            "user": getenv("DB_USER"),
            "password": getenv("DB_USER_PASSWORD"),
            "database": getenv("DB_NAME"),
        }

    @property
    def bot_token(self) -> str:
        return self._bot_token

    @property
    def totp_secret(self) -> str:
        return self._totp_secret

    @property
    def admins_ids(self) -> list[int]:
        return self._admins_ids

    @property
    def database_connection_parameters(self) -> dict[str, str]:
        return self._database_connection_parameters
