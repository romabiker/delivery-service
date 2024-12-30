import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import IdBase


class User(IdBase):
    session: Mapped[uuid.UUID] = mapped_column(default_factory=uuid.uuid4, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
    # deliveries: Mapped[list["Delivery"]] = relationship(
    #     "Delivery",
    #     back_populates="deliveries",
    #     cascade="all, delete-orphan",
    # )
