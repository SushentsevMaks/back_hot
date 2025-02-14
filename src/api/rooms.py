from datetime import date

from fastapi import APIRouter, Body, Query
from back_hot.src.api.dependencies import DBDep

from back_hot.src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2024-08-01"),
                    date_to: date = Query(example="2024-08-10")
                    ):
    check_hotel = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    # if len(check_hotel) == 0:
    #     return {"status": "ERROR", "message": "Отель не найден"}

    return check_hotel

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение одного конкретного отеля по id")
async def get_hotel(hotel_id: int, room_id: int, db: DBDep):
    check = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)

    if check is None:
        return {"status": "ERROR", "message": "Отель или номер не найден"}

    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)

@router.post("/{hotel_id}/rooms", summary="Добавление номера в отель")
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


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера из базы")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение данных номера отеля в базе")
async def put_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest, db: DBDep):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера отеля в базе")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomsPatchRequest, db: DBDep):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}




