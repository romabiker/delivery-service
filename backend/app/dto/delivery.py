from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.api.pagination import PageNumberPagination


class DeliveryCreateDTO(BaseModel):
    name: str
    user_id: int
    weight_kg: float
    cost_of_content_usd: float
    type_id: int


class DeliveryUpdateDTO(BaseModel):
    cost_of_delivery_rub: float = Field(ge=0)


class DeliveryTransportCompanyUpdateDTO(BaseModel):
    transport_company_id: int = Field(ge=0)


class DeliveryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class DeliveryTypeDTO(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        id: int
        name: str

    id: int
    name: str
    user_id: int
    weight_kg: float
    cost_of_content_usd: float
    cost_of_delivery_rub: float = 0
    type: DeliveryTypeDTO
    type_id: int
    transport_company_id: int | None
    created_at: datetime


class DeliveryApiInDTO(BaseModel):
    name: str
    weight_kg: float
    cost_of_content_usd: float
    type_id: int


class DeliveryPageNumberPagination(PageNumberPagination):
    items: list[DeliveryDTO] = Field(default_factory=list)


class DeliveryExportInClickhouseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type_id: int
    transport_company_id: int | None
    weight_kg: float
    cost_of_content_usd: float
    cost_of_delivery_rub: float = 0
    created_at: datetime


class DeliveryClickHouseStats(BaseModel):
    created: datetime
    type_id: int
    total_cost: float
