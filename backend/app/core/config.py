import secrets
from typing import Literal

from pydantic import ClickHouseDsn, MySQLDsn, RedisDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_ASYNC_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+aiomysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    # Variables for Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_USER: str | None = None
    REDIS_PASS: str | None = None
    REDIS_BASE: str | None = None

    REDIS_MAX_CONNECTIONS: int = 10

    # Variables for RabbitMQ
    RABBIT_HOST: str = "rmq"
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = "guest"
    RABBIT_PASS: str = "guest"
    RABBIT_VHOST: str = "/"

    RABBIT_POOL_SIZE: int = 2
    RABBIT_CHANNEL_POOL_SIZE: int = 10

    @property
    def REDIS_URL(self) -> URL:
        path = ""
        if self.REDIS_BASE is not None:
            path = f"/{self.REDIS_BASE}"
        return URL.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            user=self.REDIS_USER,
            password=self.REDIS_PASS,
            path=path,
        )

    @property
    def RABBIT_URL(self) -> URL:
        return URL.build(
            scheme="amqp",
            host=self.RABBIT_HOST,
            port=self.RABBIT_PORT,
            user=self.RABBIT_USER,
            password=self.RABBIT_PASS,
            path=self.RABBIT_VHOST,
        )

    AUTH_COOKIE_EXPIRE: int = 2**31 - 1

    CLICKHOUSE_HOST: str = "clickhouse"
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_USER: str = ""
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_SCHEMA: str = "clickhouse"
    CLICKHOUSE_PROTOCOL: str = "http"

    @property
    def CLICKHOUSE_URL(self) -> URL:
        return URL.build(
            scheme=self.CLICKHOUSE_SCHEMA,
            host=self.CLICKHOUSE_HOST,
            port=self.CLICKHOUSE_PORT,
            user=self.CLICKHOUSE_USER,
            password=self.CLICKHOUSE_PASSWORD,
        )


settings = Settings()  # type: ignore
