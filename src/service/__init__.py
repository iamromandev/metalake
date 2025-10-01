from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.repo import LakeRepo, get_lake_repo

from .health import HealthService
from .lake import LakeService


async def get_health_service(
) -> AsyncGenerator[HealthService]:
    yield HealthService()


async def get_lake_service(
    lake_repo: Annotated[LakeRepo, Depends(get_lake_repo)],
) -> AsyncGenerator[LakeService]:
    yield LakeService(
        lake_repo=lake_repo
    )
