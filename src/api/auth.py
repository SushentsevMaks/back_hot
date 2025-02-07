from fastapi import APIRouter, HTTPException, Response

from back_hot.src.api.dependencies import UserIdDep
from back_hot.src.database import async_session_maker
from back_hot.src.repositories.users import UsersRepository
from back_hot.src.schemas.users import UserRequestAdd, UserAdd
from back_hot.src.services.services import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login", summary="Логин юзера")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

    return {"status": "OK"}

@router.post("/register", summary="Регистрация нового пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}

@router.post("/logout", summary="Выход из системы")
async def only_auth(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK",
            "message": "Вы успешно вышли из системы"}

@router.get("/only_auth", summary="Кто мы?")
async def only_auth(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        if user is None:
            return {"status": "ERROR"}

        return user



