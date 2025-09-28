from functools import cached_property
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .type import Env


class Settings(BaseSettings):
    # core
    env: Annotated[Env, Field(description="Application environment")]
    debug: Annotated[bool, Field(description="Enable debug mode")]
    # db
    db_connection: Annotated[str, Field(description="Database connection type")]
    db_host: Annotated[str, Field(description="Database host")]
    db_port: Annotated[int, Field(description="Database port")]
    db_name: Annotated[str, Field(description="Database name")]
    db_user: Annotated[str, Field(description="Database user")]
    db_password: Annotated[str, Field(description="Database password")]
    db_root_password: Annotated[str, Field(description="Root database password")]

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
    def db_url(self) -> str:
        return f"{self.db_connection}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
