from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form


class Todo(BaseModel):
    id: Optional[int] = None
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
        return cls(item=item)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Лабораторная работа выполнена: Буриков Алексей"
            }
        }


class TodoItem(BaseModel):
    item: str


class TodoItems(BaseModel):
    todos: List[TodoItem]