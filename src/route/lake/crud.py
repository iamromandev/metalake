import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.success import Success
from src.schema import LakeOutSchema
from src.service import LakeService, get_lake_service
from src.service.auth import require_auth_key

router = APIRouter(prefix="/lake", tags=["lake"])


def _tag() -> str:
    return "lake|crud|create"


@router.post(path="")
async def create(
    service: Annotated[LakeService, Depends(get_lake_service)],
    auth_key: Annotated[str, Depends(require_auth_key)],
    app: Annotated[str, Form(...)],
    dataset: Annotated[str, Form(...)],
    ref_id: Annotated[uuid.UUID, Form(...)],
    meta: Annotated[str | None, Form(...)] = None,
    file: Annotated[UploadFile | None, File(...)] = None,
) -> JSONResponse:
    logger.debug(f"{_tag()}| app: {app}, dataset: {dataset}, ref_id: {ref_id}, meta: {meta}, file: {file}")
    data: LakeOutSchema = await service.create(
        app=app,
        dataset=dataset,
        ref_id=ref_id,
        meta=meta,
        file=file,
    )
 
    return Success.created(
        message="Lake entry created successfully.",
        data=data
    ).to_resp()
