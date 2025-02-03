from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from back_hot.src.schemas.hotels_class import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        item = result.scalars().first()
        return self.schema.model_validate(item, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        existing_item = await self.session.execute(
            select(self.model).filter_by(**filter_by)
        )
        if not existing_item.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Record not found")

        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by) -> None:
        existing_item = await self.session.execute(
            select(self.model).filter_by(**filter_by)
        )
        if not existing_item.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Record not found")

        delete_data_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )

        await self.session.execute(delete_data_stmt)

