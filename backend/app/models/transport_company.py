from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import IdBase


class TransportCompany(IdBase):
    name: Mapped[str | None] = mapped_column(String(255))
