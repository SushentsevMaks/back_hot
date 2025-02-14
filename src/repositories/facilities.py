from datetime import date

from back_hot.src.models.facilities import FacilitiesOrm
from back_hot.src.repositories.base import BaseRepository
from back_hot.src.schemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities

