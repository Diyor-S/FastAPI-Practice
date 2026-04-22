import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api import router as api_router
from core.config import settings
from core.lifespan import lifespan


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
