from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import IdBase


class Delivery(IdBase):
    """название, вес, тип, стоимость содержимого в долларах"""
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    cost_of_content_usd: Mapped[float] = mapped_column(Float, nullable=False)
    cost_of_delivery_rub: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    type_id: Mapped[int] = mapped_column(ForeignKey("deliverytypes.id"))
    type: Mapped["DeliveryType"] = relationship(  # noqa: F821
        "DeliveryType",
        lazy="joined"
    )
