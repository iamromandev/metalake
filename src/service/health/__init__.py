from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from pydantic import Field

from .health import HealthService


async def get_health_service(
 ) -> AsyncGenerator[HealthService]:
    yield HealthService( )

