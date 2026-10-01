from pydantic import BaseModel
from typing import List


# Базовая модель с ID (для создания)
class Todo(BaseModel):
    id: int
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Лабораторная работа выполнена: Буриков Алексей"
            }
        }


# Модель без ID (для обновления текста задачи через PUT)
class TodoItem(BaseModel):
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "item": "Обновленный текст задачи от Бурикова Алексея"
            }
        }


# Модель ответа (скрывает id при запросе GET /todo)
class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        json_schema_extra = {
            "example": {
                "todos": [
                    {"item": "Пример задачи 1 (Буриков Алексей)"},
                    {"item": "Пример задачи 2 (Буриков Алексей)"}
                ]
            }
        }