from fastapi import UploadFile

from src.core.base import BaseService
from src.repo import LakeRepo
from src.schema import LakeCreateSchema, LakeOutSchema


class LakeService(BaseService):
    _lake_repo: LakeRepo

    def __init__(
        self,
        lake_repo: LakeRepo,
    ) -> None:
        super().__init__()
        self._lake_repo = lake_repo

    async def create(
        self,
        payload: LakeCreateSchema,
        file: UploadFile | None = None
    ) -> LakeOutSchema:
        self._lake_repo.create(

        )

