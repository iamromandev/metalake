from functools import cached_property

from fastapi import UploadFile
from minio import Minio
from minio.datatypes import Bucket

from src.core.factory import SingletonMeta


class StorageClient(metaclass=SingletonMeta):
    _initialized: bool = False
    _client: Minio
    _part_size: int

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool,
        bucket: str,
        chunk_size: int
    ) -> None:
        if self._initialized:
            return
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self._create_bucket(bucket)
        self._part_size = chunk_size
        self._initialized = True

    @cached_property
    def _tag(self) -> str:
        return self.__class__.__name__

    def _create_bucket(self, bucket: str) -> None:
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    def _get_bucket(self) -> Bucket | None:
        buckets = self._client.list_buckets()
        return next(iter(buckets), None)

    async def store(
        self, file_key: str, file: UploadFile
    ) -> None:
        bucket = self._get_bucket()
        if not bucket:
            raise ValueError("No bucket found to store")
        self._client.put_object(
            bucket_name=bucket.name,
            object_name=file_key,
            data=file.file,
            length=-1,
            content_type=file.content_type,
            part_size=self._part_size,
        )
