from app.dao.base import DAOBase
from app.dto import DeliveryCreateDTO, DeliveryDTO, DeliveryUpdateDTO
from app.models import Delivery


class UserDAO(DAOBase[Delivery, DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryDTO]): ...


delivery_dao = UserDAO(Delivery, DeliveryDTO)
