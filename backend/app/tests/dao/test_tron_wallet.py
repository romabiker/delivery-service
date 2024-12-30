import pytest
from app.dao import tron_wallet_dao

from app.dto import TronWalletCreateDTO
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.anyio


async def test_create_tron_wallet(session: AsyncSession) -> None:
    wallet_create_dto = TronWalletCreateDTO(
        address = 'TestiwbBedv7E8p4FkyPyeqq4RVoqRL3TW',
        balance = 500.1,
        bandwidth = 1000,
        energy = 100,
    )
    tron_wallet = await tron_wallet_dao.create(session, wallet_create_dto)


    assert tron_wallet is not None
    assert tron_wallet.address == wallet_create_dto.address
    assert tron_wallet.balance == wallet_create_dto.balance
    assert tron_wallet.bandwidth == wallet_create_dto.bandwidth
    assert tron_wallet.energy == wallet_create_dto.energy
