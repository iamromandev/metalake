from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.client import StorageClient, get_storage_client
from src.repo import LakeRepo, get_lake_repo

from .health import HealthService
from .lake import LakeService


async def get_health_service(
) -> AsyncGenerator[HealthService]:
    yield HealthService()


async def get_lake_service(
    storage_client: Annotated[StorageClient, Depends(get_storage_client)],
    lake_repo: Annotated[LakeRepo, Depends(get_lake_repo)],
) -> AsyncGenerator[LakeService]:
    yield LakeService(
        storage_client=storage_client,
        lake_repo=lake_repo
    )
