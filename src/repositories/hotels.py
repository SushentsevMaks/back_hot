from sqlalchemy import select, func

from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.hotels_class import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


