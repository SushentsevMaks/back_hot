from fastapi import APIRouter
from fastapi import APIRouter, Body, Query
from back_hot.src.api.dependencies import DBDep

from back_hot.src.schemas.rooms import RoomsAdd, RoomsAddRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получение всех номеров отеля")
async def get_facilities(
                    db: DBDep
                    ):
    check_hotel = await db.facilities.get_all()

    # if len(check_hotel) == 0:
    #     return {"status": "ERROR", "message": "Отель не найден"}

    return check_hotel


@router.post("", summary="Добавление номера в отель")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomsAddRequest = Body(openapi_examples={
    "1": {
    "summary": "Example 1",
    "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "description": "ул. Моря, 1",
        "price": 2,
        "quantity": 4,
        }
    },
    "2": {
        "summary": "Example 2",
        "value": {
            "title": "Отель Dubai 5 звезд у моря",
            "description": "ул. Моря, 453",
            "price": 5,
            "quantity": 0,
        }
    }
})):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

    if hotel is None:
        return {"status": "ERROR", "message": "Отель не найден"}

    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}