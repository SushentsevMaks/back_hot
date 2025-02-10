
from fastapi import Query, APIRouter, Body
from back_hot.src.database import async_session_maker, engine
from back_hot.src.repositories.hotels import HotelsRepository

from back_hot.src.repositories.rooms import RoomsRepository
from back_hot.src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        check_hotel = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

        if len(check_hotel) == 0:
            return {"status": "ERROR", "message": "Отель не найден"}

        return check_hotel

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение одного конкретного отеля по id")
async def get_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        check = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        # check_hotel = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id)
        # check_room = await RoomsRepository(session).get_one_or_none(id=room_id)
        #
        if check is None:
            return {"status": "ERROR", "message": "Отель или номер не найден"}
        #
        # if check_room is None:
        #     return {"status": "ERROR", "message": "Номер не найден"}

        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)

@router.post("/{hotel_id}/rooms", summary="Добавление номера в отель")
async def create_room(hotel_id: int, room_data: RoomsAddRequest = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)

        if hotel is None:
            return {"status": "ERROR", "message": "Отель не найден"}

        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера из базы")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение данных номера отеля в базе")
async def put_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()

    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера отеля в базе")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomsPatchRequest):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
        await session.commit()

        return {"status": "OK"}




