from fastapi import FastAPI
from .database import engine, Base
from .routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with FastAPI",
    version="1.0.0"
)

app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "Welcome to Todo API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
