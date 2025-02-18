from pydantic import BaseModel, Field

from back_hot.src.schemas.facilities import Facilities


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomWithRels(Rooms):
    facilities: list[Facilities]


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] = []


class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
