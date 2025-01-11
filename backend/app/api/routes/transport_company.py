from fastapi import APIRouter

from app.api.deps import SessionDep
from app.dao import transport_company_dao
from app.dto import TransportCompanyCreateDTO, TransportCompanyDTO

router = APIRouter(tags=["transport-company"], prefix="/transport-company")


@router.post("", response_model=TransportCompanyDTO)
async def create(
    transport_company_in: TransportCompanyCreateDTO,
    db_session: SessionDep,
) -> TransportCompanyDTO:
    transport_company = await transport_company_dao.create(
        db_session, transport_company_in
    )
    return transport_company


@router.get("", response_model=list[TransportCompanyDTO])
async def get_list(
    db_session: SessionDep,
) -> list[TransportCompanyDTO]:
    items = await transport_company_dao.get_list(db_session)
    return items
