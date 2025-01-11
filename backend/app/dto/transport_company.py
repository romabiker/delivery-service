from pydantic import BaseModel, ConfigDict


class TransportCompanyCreateDTO(BaseModel):
    name: str


class TransportCompanyUpdateDTO(BaseModel):
    name: str


class TransportCompanyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
