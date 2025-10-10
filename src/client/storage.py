from functools import cached_property

from fastapi import UploadFile
from loguru import logger
from minio import Minio
from minio.datatypes import Bucket
from pydantic import HttpUrl

from src.core.factory import SingletonMeta
from src.schema import FileSchema


class StorageClient(metaclass=SingletonMeta):
    _initialized: bool = False
    _client: Minio
    _endpoint: str
    _secure: bool
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
        self._endpoint = endpoint
        self._secure = secure
        self._part_size = chunk_size
        self._initialized = True

    @cached_property
    def _tag(self) -> str:
        return self.__class__.__name__

    @cached_property
    def _base_url(self) -> str:
        scheme = "https" if self._secure else "http"
        return f"{scheme}://{self._endpoint}"

    def _create_bucket(self, bucket: str) -> None:
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    def _get_bucket(self) -> Bucket | None:
        buckets = self._client.list_buckets()
        return next(iter(buckets), None)

    async def store(
        self, file_key: str, file: UploadFile
    ) -> FileSchema:
        bucket = self._get_bucket()
        if not bucket:
            raise ValueError("No bucket found to store")
        result = self._client.put_object(
            bucket_name=bucket.name,
            object_name=file_key,
            data=file.file,
            length=-1,
            content_type=file.content_type,
            part_size=self._part_size,
        )
        logger.debug(f"{self._tag}|store(): Stored file {file_key} at {result}")
        return FileSchema(
            name=file.filename,
            size=file.size,
            content_type=file.content_type,
            url=HttpUrl(
                url=f"{self._base_url}/{bucket.name}/{file_key}"
            )
        )
