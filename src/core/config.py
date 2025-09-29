from functools import cached_property
from typing import Annotated
from urllib.parse import quote_plus

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from .formats import serialize
from .type import Env


class Settings(BaseSettings):
    # core
    env: Annotated[Env, Field(description="Application environment")]
    debug: Annotated[bool, Field(description="Enable debug mode")]
    # db
    db_schema: Annotated[str, Field(description="Database connection type")]
    db_user: Annotated[str, Field(description="Database user")]
    db_password: Annotated[SecretStr, Field(description="Database password")]
    db_root_password: Annotated[SecretStr, Field(description="Database root password")]
    db_host: Annotated[str, Field(description="Database host")]
    db_port: Annotated[int, Field(description="Database port")]
    db_name: Annotated[str, Field(description="Database name")]
    # storage
    storage_root_user: Annotated[str, Field(description="Storage root user")]
    storage_root_password: Annotated[SecretStr, Field(description="Storage root password")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

    @cached_property
    def is_local(self) -> bool:
        return self.env == Env.LOCAL

    @cached_property
    def is_prod(self) -> bool:
        return self.env == Env.PROD

    @cached_property
    def db_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.db_schema,
            username=self.db_user,
            password=quote_plus(serialize(self.db_password)),
            host=self.db_host,
            port=self.db_port,
            path=self.db_name
        )


settings = Settings()
