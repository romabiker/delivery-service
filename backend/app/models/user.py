import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import IdBase


def generate_uuid():
    return str(uuid.uuid4())


class User(IdBase):
    session: Mapped[str] = mapped_column(String(255), default=generate_uuid, nullable=False, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
