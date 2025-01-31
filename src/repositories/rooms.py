from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsOrm