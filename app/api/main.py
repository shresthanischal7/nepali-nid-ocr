from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.ocr.paddle_engine import PaddleEngine
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Load PaddleOCR once during startup
    PaddleEngine.initialize_model()

    yield

    print("Application shutting down.")


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")