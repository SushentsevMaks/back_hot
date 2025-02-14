from datetime import date

from back_hot.src.models.bookings import BookingsOrm
from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.repositories.utils import rooms_ids_for_booking
from back_hot.src.schemas.rooms import Rooms
from sqlalchemy import select, func


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all(self, title):
        query = select(self.model)
        query = query.where(self.model.title.ilike(f"%{title.lower()}%"))
        result = await self.session.execute(query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))