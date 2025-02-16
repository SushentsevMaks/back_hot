from fastapi import APIRouter
from fastapi import APIRouter, Body, Query
from back_hot.src.api.dependencies import DBDep
from back_hot.src.schemas.facilities import FacilitiesAdd

from back_hot.src.schemas.rooms import RoomsAdd, RoomsAddRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получение всех удобств отеля")
async def get_facilities(db: DBDep):
    check_hotel = await db.facilities.get_all()
    return check_hotel


@router.post("", summary="Добавление нового удобства")
async def create_room(facilities_data: FacilitiesAdd, db: DBDep):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "OK", "data": facilities}