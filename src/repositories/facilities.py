from datetime import date

from pydantic import BaseModel
from sqlalchemy import update

from back_hot.src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.facilities import Facilities, RoomFacilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilities

    async def edit(self, data: list) -> None:
        add_data_stmt = update(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)
