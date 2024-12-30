from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeliveryCreateDTO(BaseModel):
    name: str
    user_id: int
    weight_kg: float
    cost_of_content_usd: float
    type_id: int


class DeliveryUpdateDTO(BaseModel):
    cost_of_delivery_rub: float


class DeliveryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int
    weight_kg: float
    cost_of_content_usd: float
    cost_of_delivery_rub: float = 0
    type_id: int
    created_at: datetime
    updated_at: datetime


class DeliveryApiInDTO(BaseModel):
    name: str
    weight_kg: float
    cost_of_content_usd: float
    type_id: int
