from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn, NewUser

user_router = APIRouter(tags=["User"])

# Временная база данных пользователей в памяти
users = {}


# Регистрация пользователя
@user_router.post("/signup")
async def sign_new_user(data: NewUser) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует (Буриков Алексей)"
        )
    users[data.email] = data
    return {"message": "Пользователь успешно зарегистрирован (Буриков Алексей)!"}


# Авторизация пользователя
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден (Буриков Алексей)"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверные учетные данные (пароль не совпадает)"
        )
    return {"message": "Успешный вход в систему (Буриков Алексей)"}