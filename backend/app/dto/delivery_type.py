from pydantic import BaseModel, ConfigDict


class DeliveryTypeCreateDTO(BaseModel):
    name: str


class DeliveryTypeUpdateDTO(BaseModel):
    name: str


class DeliveryTypeDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
