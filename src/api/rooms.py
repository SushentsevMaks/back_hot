
from fastapi import Query, APIRouter, Body
from back_hot.src.api.dependencies import PaginationDep
from back_hot.src.database import async_session_maker, engine

from back_hot.src.repositories.rooms import RoomsRepository
from back_hot.src.schemas.rooms import RoomsPATCH, RoomsAdd, Rooms

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])

@router.get("", summary="Получение всех номеров отеля")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.get("/{room_id}", summary="Получение одного конкретного отеля по id")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=hotel_id)

@router.post("", summary="Добавление номера в отель")
async def create_room(hotel_id: int, room_data: RoomsAdd = Body(openapi_examples={
    "1": {
    "summary": "Сочи",
    "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "description": "ул. Моря, 1",
        "price": 2,
        "quantity": 4,
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Dubai 5 звезд у моря",
            "description": "ул. Моря, 453",
            "price": 5,
            "quantity": 0,
        }
    }
})):

    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id)

        if hotel is None:
            return {"status": "ERROR"}

        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.delete("/{room_id}", summary="Удаление отеля из базы")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}

@router.put("/{room_id}", summary="Полное изменение данных отеля в базе")
async def put_hotel(hotel_id: int, hotel_data: RoomsAdd):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}

@router.patch("/{room_id}", summary="Частичное изменение данных отеля в базе")
async def patch_hotel(hotel_id: int, hotel_data: RoomsPATCH):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()

        return {"status": "OK"}




