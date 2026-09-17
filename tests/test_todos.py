import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from unittest.mock import patch

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo.db"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Купить молоко", "description": "В магазине", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Купить молоко"
    assert "id" in data

def test_read_todos():
    client.post("/todos/", json={"title": "Задача 1", "description": "Описание", "completed": False})
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_read_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch('app.crud.notifications.send_notification')
def test_create_todo_sends_notification(mock_send_notification):
    mock_send_notification.return_value = True
    response = client.post(
        "/todos/",
        json={"title": "Важная задача", "description": "Проверка мока", "completed": False}
    )
    assert response.status_code == 201
    mock_send_notification.assert_called_once_with("Важная задача")
