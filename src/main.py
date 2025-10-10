from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.common import get_app_version
from src.core.config import settings
from src.core.error import config_global_errors
from src.db import init_db, run_migrations
from src.route.health import health_router
from src.route.lake import lake_crud_router


@asynccontextmanager
async def lifespan(fa: FastAPI):
    await run_migrations()
    yield  # startup complete
    # any shutdown code here


app = FastAPI(
    title="Metalake Application",
    version=get_app_version(),
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# error
config_global_errors(app)
# database
init_db(app)

# health check
app.include_router(health_router)
# lake crud
app.include_router(lake_crud_router)
