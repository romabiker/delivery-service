from app.dao.base import DAOBase
from app.dto import (
    TransportCompanyCreateDTO,
    TransportCompanyDTO,
    TransportCompanyUpdateDTO,
)
from app.models import TransportCompany


class TransportCompanyDAO(
    DAOBase[
        TransportCompany,
        TransportCompanyCreateDTO,
        TransportCompanyUpdateDTO,
        TransportCompanyDTO,
    ]
): ...


transport_company_dao = TransportCompanyDAO(TransportCompany, TransportCompanyDTO)
