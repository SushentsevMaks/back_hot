
from fastapi import Query, APIRouter
from back_hot.src.api.dependencies import PaginationDep
from back_hot.src.schemas.hotels_class import Hotel, HotelPATCH

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router_hotels.get("", summary="Получение всех отелей")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),

):
    hotels_ = []
    if id is not None or title is not None:
        for hotel in hotels:
            if id is not None and hotel["id"] != id:
                continue
            if title is not None and hotel["title"] != title:
                continue
            hotels_.append(hotel)
        return hotels_

    return hotels[(pagination.page-1)*pagination.per_page:pagination.page*pagination.per_page]




@router_hotels.post("", summary="Добавления отеля в базу")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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



