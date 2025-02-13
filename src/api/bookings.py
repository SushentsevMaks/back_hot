
from fastapi import APIRouter, Body, HTTPException
from back_hot.src.api.dependencies import DBDep, UserIdDep, PaginationDep
from back_hot.src.schemas.bookings import BookingsAdd, Bookings, BookingsAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", summary="Получение всех бронирований")
async def get_bookings(
        pagination: PaginationDep,
        db: DBDep
):
    per_page = pagination.per_page or 5

    return await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/me", summary="Получение всех бронирований конкретного пользователя")
async def get_bookings_me(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавления брони в базу")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingsAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Example 1",
        "value": {
            "room_id": 1,
            "date_from": "2024-10-01",
            "date_to": "2024-10-10"
                }
        },
    "2": {
        "summary": "Example 2",
        "value": {
            "room_id": 3,
            "date_from": "2023-12-03",
            "date_to": "2023-12-23"
        }
    }
})):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Такого номера не существует")

    _booking_data = BookingsAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
