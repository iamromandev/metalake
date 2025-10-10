from typing import Annotated, Any

from pydantic import Field
from tortoise.contrib.pydantic import pydantic_model_creator

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


class LakeOutSchema(_LakeOutSchema):
    pass
