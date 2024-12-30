from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import IdBase


class DeliveryType(IdBase):
    """Посылки бывают 3х типов: одежда, электроника, разное.
    Типы должны храниться в отдельной таблице в базе данных.
    """
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
