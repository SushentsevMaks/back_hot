from pydantic import EmailStr
from sqlalchemy import select

from back_hot.src.models.users import UsersOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        item = result.scalars().one()
        return UserWithHashedPassword.model_validate(item, from_attributes=True)