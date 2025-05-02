import pytest

@pytest.mark.asyncio
async def test_auth(client):
    responce = await client.post(
        "/login",
        data={
            "username": "test_user",
            "password": "12345"
        }
    )
    assert responce.status_code == 403
    assert responce.json() == {'detail': 'Invalid Credentials'}
