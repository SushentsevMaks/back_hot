from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilities(RoomFacilitiesAdd):
    id: int
