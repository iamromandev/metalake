from collections.abc import AsyncGenerator

from src.client.storage import StorageClient
from src.core.config import settings


async def get_storage_client() -> AsyncGenerator[StorageClient]:
    yield StorageClient(
        endpoint=settings.storage_endpoint,
        access_key=settings.storage_root_user,
        secret_key=settings.storage_root_password.get_secret_value(),
        secure=settings.storage_secure,
        bucket=settings.storage_bucket,
        chunk_size=settings.storage_chunk_size
    )
