import pytest
from httpx import AsyncClient

BASE_URL='/api/schedule/'

audience_ids = [142, 143, 251, 252, 253, 254, 255, 339, 340, 341, 342, 343]

some_json_test = {   
    "audience_id": "251",
    "subject": "Математика",
    "teacher": "Шерстнева",
    "start_time": "20:00",
    "end_time": "22:00",
    "date": "2025-09-09"
}

@pytest.mark.asyncio
@pytest.mark.parametrize("audience_id", audience_ids)
async def test_get_week_schedule(
    client: AsyncClient,
    audience_id: int
):
    #Проверка статуса и ответа

    response = await client.get(
        f"{BASE_URL}{audience_id}/week/2025-04-04"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []

@pytest.mark.asyncio
@pytest.mark.parametrize("audience_id", audience_ids)
async def test_get_week_schedule_incorrect_date(
    client: AsyncClient,
    audience_id: int
):
    #Проверка статуса и ответа

    response = await client.get(
        f"{BASE_URL}{audience_id}/week/2025-04-0"
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_schedule_not_admin(client: AsyncClient):
    login_responce = await client.post(
        "/login",
        data={
            "username": "user1234543124",
            "password": "newbie123!"
        }
    )
    assert login_responce.status_code == 200
    token = login_responce.json()["access_token"]

    responce = await client.post(
        BASE_URL,
        json=some_json_test,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert responce.status_code == 403
    assert responce.json() == {"detail": "Отказано в доступе"}


@pytest.mark.asyncio
async def test_admin_can_create_schedule(client: AsyncClient, create_test_admin):
    # Логинимся как админ
    login_res = await client.post(
    "/login", 
    data={
        "username": "test_admin", 
        "password": "adminpass123"
        })
    
    token = login_res.json()["access_token"]
    
    # Тест создания расписания
    response = await client.post(
        BASE_URL,
        json=some_json_test,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_update_schedule(client: AsyncClient, create_test_admin):
    # Логинимся как админ
    login_res = await client.post(
    "/login", 
    data={
        "username": "test_admin", 
        "password": "adminpass123"
        })
    
    token = login_res.json()["access_token"]
    
    # Тест редактирования расписания
    response = await client.put(
        f"{BASE_URL}251/1",
        json=some_json_test,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_update_schedule_incorrect(client: AsyncClient, create_test_admin):
    # Логинимся как админ
    login_res = await client.post(
    "/login", 
    data={
        "username": "test_admin", 
        "password": "adminpass123"
        })
    
    token = login_res.json()["access_token"]
    
    # Тест редактирования расписания
    response = await client.put(
        f"{BASE_URL}2511/1",
        json=some_json_test,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

