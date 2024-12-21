import uvicorn
from fastapi import FastAPI

from core.settings import settings


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
