import json
from fastapi_cache.decorator import cache
from fastapi import APIRouter
from back_hot.src.api.dependencies import DBDep

from back_hot.src.schemas.facilities import FacilitiesAdd
from back_hot.src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получение всех удобств отеля")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()



@router.post("", summary="Добавление нового удобства")
async def create_room(facilities_data: FacilitiesAdd, db: DBDep):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facilities}