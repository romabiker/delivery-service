import pytest

from app.dto import TronWalletApiInDTO
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_crud(client: AsyncClient) -> None:
    wallet_in = TronWalletApiInDTO(address='TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW')
    response = await client.post("/tron-wallet", json=wallet_in.model_dump())
    assert response.status_code == 201
    
    response = await client.get(f"/tron-wallet/{wallet_in.address}")
    assert response.status_code == 200
    assert response.json()['address'] == wallet_in.address

    response = await client.get(f"/tron-wallet")
    assert response.status_code == 200
    assert response.json()['total'] == 1
    assert response.json()['items'][0]['address'] == wallet_in.address
    
    response = await client.delete(f"/tron-wallet/{wallet_in.address}")
    assert response.status_code == 204
