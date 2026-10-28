import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_create_todo(client):
    response = await client.post(
        "/todos/",
        json={"title": "Купить молоко", "description": "В магазине", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Купить молоко"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_todos(client):
    await client.post("/todos/", json={"title": "Задача 1", "completed": False})
    response = await client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

@pytest.mark.asyncio
async def test_read_todo_not_found(client):
    response = await client.get("/todos/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
@patch('app.crud.notifications.send_notification', new_callable=AsyncMock)
async def test_create_todo_sends_notification(mock_send_notification):
    mock_send_notification.return_value = True
    response = await client.post(
        "/todos/",
        json={"title": "Важная задача", "description": "Проверка мока", "completed": False}
    )
    assert response.status_code == 201
    mock_send_notification.assert_called_once_with("Важная задача")
