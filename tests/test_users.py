import pytest
from httpx import AsyncClient

BASE_URL = "/users/"

@pytest.mark.asyncio
async def test_create_user(
    client: AsyncClient
):
    # 1. Подготовка тестовых данных
    test_data = {
        "username": "user1234543",
        "password": "newbie123!",
    }

    # 2. Выполнение запроса
    response = await client.post(
        BASE_URL,
        json=test_data
    )

    # 3. Проверка ответа
    assert response.status_code == 201, response.text
    
    response_data = response.json()
    assert "id" in response_data
    assert response_data["username"] == test_data["username"]
    assert "created_at" in response_data

@pytest.mark.asyncio
async def test_create_user_incorrect(
    client: AsyncClient,
    close_
):
    # 1. Подготовка тестовых данных
    test_data = {
        "username": "user12345",
        "password": "newbie123!",
    }

    # 2. Выполнение запроса
    response = await client.post(
        BASE_URL,
        json=test_data
    )

    # 3. Проверка ответа
    assert response.status_code == 400, response.text
    
    response_data = response.json()
    assert response_data == {"detail": "Username already exists"}
