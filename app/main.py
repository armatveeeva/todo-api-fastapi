import logging

from fastapi import FastAPI

from .routers import todos

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

logger.info("Инициализация приложения FastAPI...")

app = FastAPI(
    title="Todo API",
    description="Production-ready Todo API with async DB, layered architecture, and strict validation.",
    version="1.0.0",
)

app.include_router(todos.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Production-Ready Todo API!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
