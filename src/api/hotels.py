
from fastapi import Query, APIRouter, Body
from back_hot.src.api.dependencies import PaginationDep
from back_hot.src.database import async_session_maker, engine
from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.schemas.hotels_class import Hotel, HotelPATCH
from sqlalchemy import insert, select

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])

@router_hotels.get("", summary="Получение всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.like(f'%{location}%'))
        if title:
            query = query.filter(HotelsOrm.title.like(f'%{title}%'))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels



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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        """Дебаг sql запроса"""
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля из базы")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router_hotels.put("/{hotel_id}", summary="Полное изменение данных отеля в базе")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}

    if hotel_id > len(hotels):
        return {"status": "ERROR"}

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



