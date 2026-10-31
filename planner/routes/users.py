from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)


# Регистрация пользователя в MongoDB
@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с данным email уже существует в MongoDB"
        )
    await user_database.save(user)
    return {"message": "Пользователь успешно сохранен в MongoDB (Буриков Алексей)"}


# Авторизация
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким email не найден"
        )
    if user_exist.password == user.password:
        return {"message": "Успешная авторизация в MongoDB (Буриков Алексей)"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный пароль"
    )