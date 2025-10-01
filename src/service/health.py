from src.core.base import BaseService
from src.core.common import get_app_version
from src.core.type import Status
from src.db import get_db_health
from src.schema import HealthSchema


class HealthService(BaseService):

    def __init__(self) -> None:
        super().__init__()

    async def check_health(self) -> HealthSchema:
        app_version = get_app_version()
        db_status = Status.SUCCESS if await get_db_health() else Status.ERROR
        health: HealthSchema = HealthSchema(
            version=app_version, db=db_status
        )
        health.log()
        return health
