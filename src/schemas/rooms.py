from pydantic import BaseModel, Field

class RoomsAddRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Rooms(RoomsAdd):
    id: int

class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
