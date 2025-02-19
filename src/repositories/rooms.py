from datetime import date

from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from back_hot.src.repositories.utils import rooms_ids_for_booking
from back_hot.src.schemas.rooms import Rooms, RoomWithRels
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_all(self, title):
        query = select(self.model)
        query = query.where(self.model.title.ilike(f"%{title.lower()}%"))
        result = await self.session.execute(query)
        return [RoomDataMapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(item)

