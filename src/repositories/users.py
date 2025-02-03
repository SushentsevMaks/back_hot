from back_hot.src.models.users import UsersOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User