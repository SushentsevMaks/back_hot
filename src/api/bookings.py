
from fastapi import APIRouter, Body
from back_hot.src.api.dependencies import DBDep, UserIdDep
from back_hot.src.schemas.bookings import BookingsAdd, Bookings, BookingsAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

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

    temp_booking = db.bookings.model(
        room_id=booking_data.room_id,
        user_id=user_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room.price
    )
    total_cost = temp_booking.total_cost

    _booking_data = BookingsAdd(user_id=user_id, price=total_cost, **booking_data.model_dump())
    await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK"}
