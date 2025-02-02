
from fastapi import Query, APIRouter, Body
from back_hot.src.api.dependencies import PaginationDep
from back_hot.src.database import async_session_maker, engine
from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.repositories.hotels import HotelsRepository
from back_hot.src.schemas.hotels_class import Hotel, HotelPATCH
from sqlalchemy import insert, select, func

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])

@router_hotels.get("", summary="Получение всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router_hotels.post("", summary="Добавления отеля в базу")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
    "summary": "Сочи",
    "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
        }
    }
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля из базы")
async def delete_hotel(hotel_id: int):

    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(hotel_id)
        await session.commit()

    return {"status": "OK"}

@router_hotels.put("/{hotel_id}", summary="Полное изменение данных отеля в базе")
async def put_hotel(hotel_id: int, hotel_data: Hotel):

    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, hotel_id)
        await session.commit()

    return {"status": "OK"}

@router_hotels.patch("/{hotel_id}", summary="Частичное изменение данных отеля в базе")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name

            return {"status": "OK"}

    if hotel_id > len(hotels):
        return {"status": "ERROR"}



