from datetime import date

from fastapi import Query, APIRouter, Body
from back_hot.src.api.dependencies import PaginationDep, DBDep
from back_hot.src.schemas.hotels_class import HotelPATCH, HotelAdd

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])

@router_hotels.get("", summary="Получение всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router_hotels.get("/{hotel_id}", summary="Получение одного конкретного отеля по id")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router_hotels.post("", summary="Добавления отеля в базу")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля из базы")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router_hotels.put("/{hotel_id}", summary="Полное изменение данных отеля в базе")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router_hotels.patch("/{hotel_id}", summary="Частичное изменение данных отеля в базе")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}




