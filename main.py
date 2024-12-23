import uvicorn
from fastapi import FastAPI

from api import api_router
from core.settings import settings


app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
