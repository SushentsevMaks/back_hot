from back_hot.src.models.bookings import BookingsOrm
from back_hot.src.models.hotels import HotelsOrm
from back_hot.src.models.rooms import RoomsOrm
from back_hot.src.models.users import UsersOrm
from back_hot.src.repositories.mappers.base import DataMapper
from back_hot.src.schemas.bookings import Bookings
from back_hot.src.schemas.hotels_class import Hotel
from back_hot.src.schemas.rooms import Rooms, RoomWithRels
from back_hot.src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings
