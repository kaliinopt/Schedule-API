import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user_for_auth(client: AsyncClient):
    # 1. Подготовка тестовых данных
    test_data = {
        "username": "user1234543124",
        "password": "newbie123!",
    }

    # 2. Выполнение запроса
    response = await client.post("/users/", json=test_data)

    # 3. Проверка ответа
    assert response.status_code == 201, response.text

    response_data = response.json()
    assert "id" in response_data
    assert response_data["username"] == test_data["username"]
    assert "created_at" in response_data


@pytest.mark.asyncio
async def test_auth_incorrect(client):
    responce = await client.post(
        "/login", data={"username": "test_user", "password": "12345"}
    )
    assert responce.status_code == 403
    assert responce.json() == {"detail": "Invalid Credentials"}


@pytest.mark.asyncio
async def test_auth(client):
    responce = await client.post(
        "/login", data={"username": "user1234543124", "password": "newbie123!"}
    )
    assert responce.status_code == 200
    assert "access_token" in responce.json()
