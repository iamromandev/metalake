from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from loguru import logger

from src.core.config import settings
from src.core.error import Error

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(
    api_key: Annotated[str, Depends(api_key_header)]
) -> str:
    logger.debug(f"verify_api_key(): api_key {api_key}")
    if api_key != settings.api_key.get_secret_value():
        raise Error.unauthorized(
            message="Unauthorized"
        )
    return api_key
