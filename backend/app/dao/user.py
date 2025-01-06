from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import DAOBase
from app.dto import UserCreateDTO, UserDTO, UserUpdateDTO
from app.models import User


class UserDAO(DAOBase[User, UserCreateDTO, UserUpdateDTO, UserDTO]):
    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid_str: str,
    ) -> UserDTO | None:
        res = await db.execute(select(self.model).where(self.model.session == uuid_str))
        orm_obj = res.scalars().one_or_none()
        if orm_obj:
            return self.item_dto_cls.model_validate(orm_obj)


user_dao = UserDAO(User, UserDTO)
