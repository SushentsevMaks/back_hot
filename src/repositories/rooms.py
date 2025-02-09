from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.rooms import Rooms
from sqlalchemy import select, insert, update, delete
from fastapi import HTTPException


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

