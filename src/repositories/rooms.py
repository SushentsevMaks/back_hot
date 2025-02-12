from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.rooms import Rooms
from sqlalchemy import select


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all(self, title):
        query = select(self.model)
        query = query.where(self.model.title.ilike(f"%{title.lower()}%"))
        result = await self.session.execute(query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]


