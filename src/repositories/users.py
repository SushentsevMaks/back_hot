from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select

from back_hot.src.database import engine
from back_hot.src.models.users import UsersOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

        return UserWithHashedPassword.model_validate(user, from_attributes=True)