from typing import Annotated, Any

from pydantic import Field, HttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator

from src.core.base import BaseSchema
from src.db.model import Lake

_LakeCreateSchema = pydantic_model_creator(
    Lake,
    name="LakeCreate",
    exclude_readonly=True,
    exclude=("ref_id",)
)


class LakeCreateSchema(_LakeCreateSchema):
    data: Annotated[dict[str, Any] | list[Any] | str | None, Field(...)] = Field(default=None)


LakeUpdateSchema = pydantic_model_creator(
    Lake,
    name="LakeUpdate",
    exclude_readonly=True
)

_LakeOutSchema = pydantic_model_creator(
    Lake,
    name="LakeOut",
    exclude_readonly=True
)


class FileSchema(BaseSchema):
    name: Annotated[str, Field(...)]
    size: Annotated[int, Field(...)]
    content_type: Annotated[str, Field(...)]
    url: Annotated[HttpUrl | None, Field(...)] = Field(default=None)


class LakeOutSchema(_LakeOutSchema):
    pass
    # file: Annotated[FileSchema | None, Field(...)] = Field(default=None)
    #
    # @classmethod
    # async def from_orm_with_file(
    #     cls, lake: Lake, file: FileSchema
    # ) -> Self:
    #     base = await cls.from_tortoise_orm(lake)
    #
    #     return base.model_copy(update={
    #
    #     })
