from datetime import date

from pydantic import BaseModel
from sqlalchemy import update, select, delete, insert

from back_hot.src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.facilities import Facilities, RoomFacilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilities

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = res.scalars().all()

        if len(facilities_ids) > 0:
            ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        else:
            ids_to_delete: list[int] = []

        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if len(ids_to_delete) > 0:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if len(ids_to_insert) > 0:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)