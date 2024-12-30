from app.dao.base import DAOBase
from app.dto import UserCreateDTO, UserDTO, UserUpdateDTO
from app.models import User


class UserDAO(DAOBase[User, UserCreateDTO, UserUpdateDTO, UserDTO]): ...


user_dao = UserDAO(User, UserDTO)
