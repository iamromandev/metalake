import json
import uuid

from fastapi import UploadFile

from src.client import StorageClient
from src.core.base import BaseService
from src.core.error import Error
from src.repo import LakeRepo
from src.schema import LakeOutSchema


class LakeService(BaseService):
    _storage_client: StorageClient
    _lake_repo: LakeRepo

    def __init__(
        self,
        storage_client: StorageClient,
        lake_repo: LakeRepo,
    ) -> None:
        super().__init__()
        self._storage_client = storage_client
        self._lake_repo = lake_repo

    async def create(
        self,
        app: str,
        dataset: str,
        ref_id: uuid.UUID,
        meta: str | None = None,
        file: UploadFile | None = None,
    ) -> LakeOutSchema:
        db_lake = await self._lake_repo.first(
            app=app,
            dataset=dataset,
            ref_id=ref_id,
        )
        if db_lake:
            raise Error.bad_request(
                message="Lake entry already exists for the given app, dataset, and ref_id."
            )
        metadata = json.loads(meta) if meta else None
        db_lake = await self._lake_repo.create(
            app=app, dataset=dataset, ref_id=ref_id, meta=metadata
        )
        if file:
            await self._storage_client.store(
                file_key=db_lake.file_key(file),
                file=file,
            )
