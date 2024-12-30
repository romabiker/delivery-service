import secrets
from typing import Literal

from pydantic import (
    computed_field,
    MySQLDsn,
    RedisDsn
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    DEBUG: bool = True
    ROOT_PATH: str = ""
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str
    MYSQL_SERVER: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""

    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
    #     return MultiHostUrl.build(
    #         scheme="postgresql+psycopg",
    #         username=self.POSTGRES_USER,
    #         password=self.POSTGRES_PASSWORD,
    #         host=self.POSTGRES_SERVER,
    #         port=self.POSTGRES_PORT,
    #         path=self.POSTGRES_DB,
    #     )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_ASYNC_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+aiomysql",
            username=self.MYSQl_USER,
            password=self.MYSQl_PASSWORD,
            host=self.MYSQl_SERVER,
            port=self.MYSQl_PORT,
            path=self.MYSQl_DB,
            query="charset=utf8mb4"
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    REDIS_URL: RedisDsn = "redis://redis:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10


settings = Settings()  # type: ignore
