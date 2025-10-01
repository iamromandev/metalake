from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from src.schema.lake import LakeCreateSchema
from src.service import LakeService, get_lake_service
from src.service.auth import verify_api_key

router = APIRouter(prefix="/lake", tags=["lake"])


@router.post(path="")
async def create(
    api_key: Annotated[str, Depends(verify_api_key)],
    payload: Annotated[LakeCreateSchema, Body(...)],
    file: Annotated[UploadFile | None, File(...)],
    service: Annotated[LakeService, Depends(get_lake_service)],
) -> JSONResponse:
    pass
    # output: CollectionOutSchema = await service.create_data(
    #      user=user, payload=payload
    # )
    # return Success.created(
    #     message="Collection created successfully.",
    #     data=output
    # ).to_resp()
