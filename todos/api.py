from fastapi import FastAPI
from todo import todo_router

app = FastAPI(
    title="Todo API",
    description="Практическая работа №4: Маршрутизация в FastAPI. Выполнил: Буриков Алексей"
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Добро пожаловать в API студента: Буриков Алексей"}


# Подключение маршрутизатора из todo.py
app.include_router(todo_router)