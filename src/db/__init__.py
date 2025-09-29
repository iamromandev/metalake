import asyncio
from urllib.parse import quote_plus

from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src.core.config import settings
from src.core.formats import serialize

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": settings.db_host,
                "port": settings.db_port,
                "database": settings.db_name,
                "user": settings.db_user,
                "password": serialize(settings.db_password),
            }
        }
    },
    "apps": {
        "models": {
            "models": ["src.db.model"],
            "default_connection": "default",
        },
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",
        }
    }
}


def init_db(fa: FastAPI) -> None:
    register_tortoise(
        fa,
        config=DB_CONFIG,
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def init_db_for_taskiq() -> None:
    await Tortoise.init(config=DB_CONFIG)


async def close_db() -> None:
    await Tortoise.close_connections()


async def run_migrations() -> None:
    async def run_command(*args):
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.debug(f"Command {' '.join(args)} failed with error:\n{stderr.decode().strip()}")
        else:
            logger.debug(f"Command {' '.join(args)} succeeded:\n{stdout.decode().strip()}")

        return process.returncode

    # Step 1: aerich init-db (only initializes if DB is empty)
    rc_init = await run_command("aerich", "init-db")
    if rc_init != 0:
        logger.warning("Skipping `aerich upgrade` because `aerich init-db` failed.")
        return

    # Step 2: aerich upgrade
    await run_command("aerich", "upgrade")


async def get_db_health() -> bool:
    try:
        await Tortoise.get_connection("default").execute_script("SELECT 1;")
        return True
    except Exception as error:
        logger.error(f"Error|get_db_health(): {str(error)}")
        return False
