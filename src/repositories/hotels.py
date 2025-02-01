from sqlalchemy import select, func, insert

from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
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
        return result.scalars().all()

    async def add(
            self,
            title,
            location
    ):

        query = insert(self.model).values(title=title, location=location).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().first()