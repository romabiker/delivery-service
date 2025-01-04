from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session: str
    full_name: str | None


class UserCreateDTO(BaseModel):
    session: str
    full_name: str | None


class UserUpdateDTO(BaseModel):
    session: str
    full_name: str | None
