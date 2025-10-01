from collections.abc import AsyncGenerator

from src.repo.lake import LakeRepo


async def get_lake_repo() -> AsyncGenerator[LakeRepo]:
    yield LakeRepo()