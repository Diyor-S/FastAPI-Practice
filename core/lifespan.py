from contextlib import asynccontextmanager
from core.models import db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start
    yield
    # Shutdown
    await db_helper.dispose()
