
from fastapi import Query, Body, APIRouter

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]

@router_hotels.get("", summary="Получение всех отелей")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router_hotels.post("", summary="Добавления отеля в базу")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля из базы")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router_hotels.put("/{hotel_id}", summary="Полное изменение отеля в базе")
def put_hotel(hotel_id: int, hotel_title: str, hotel_name: str):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_title
            hotel["name"] = hotel_name

            return {"status": "OK"}

    if hotel_id > len(hotels):
        return {"status": "ERROR"}

@router_hotels.patch("/{hotel_id}", summary="Частичное изменение отеля в базе")
def patch_hotel(hotel_id: int, hotel_title: str | None, hotel_name: str | None):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_title is not None:
                hotel["title"] = hotel_title
            if hotel_name is not None:
                hotel["name"] = hotel_name

            return {"status": "OK"}

    if hotel_id > len(hotels):
        return {"status": "ERROR"}



