from datetime import date

from sqlalchemy import select, func

from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.repositories.mappers.mappers import HotelDataMapper
from back_hot.src.repositories.utils import rooms_ids_for_booking
from back_hot.src.schemas.hotels_class import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:
        query = select(HotelsOrm)

        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f'%{location.lower()}%'))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f'%{title.lower()}%'))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [HotelDataMapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))

        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f'%{location.lower()}%'))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f'%{title.lower()}%'))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
