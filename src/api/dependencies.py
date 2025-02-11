from typing import Annotated
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from back_hot.src.database import async_session_maker
from back_hot.src.services.services import AuthService
from back_hot.src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(3, ge=3, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]