from pydantic import BaseModel, Field

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Rooms(RoomsAdd):
    id: int


class RoomsPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
