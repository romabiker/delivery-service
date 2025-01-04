from app.dao.base import DAOBase
from app.dto import DeliveryCreateDTO, DeliveryDTO, DeliveryUpdateDTO
from app.models import Delivery


class DeliveryDAO(DAOBase[Delivery, DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryDTO]): ...


delivery_dao = DeliveryDAO(Delivery, DeliveryDTO)
