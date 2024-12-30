from app.dao.base import DAOBase
from app.dto import DeliveryTypeCreateDTO, DeliveryTypeDTO, DeliveryTypeUpdateDTO
from app.models import DeliveryType


class UserDAO(DAOBase[DeliveryType, DeliveryTypeCreateDTO, DeliveryTypeUpdateDTO, DeliveryTypeDTO]): ...


delivery_type_dao = UserDAO(DeliveryType, DeliveryTypeDTO)
