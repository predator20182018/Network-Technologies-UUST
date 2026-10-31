from beanie import Document
from pydantic import BaseModel
from typing import Optional, List


# 1. Документ MongoDB
class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"  # Имя коллекции в MongoDB

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI & MongoDB Event (Буриков Алексей)",
                "image": "https://linktomyimage.com/image.png",
                "description": "Презентация книги по FastAPI с NoSQL MongoDB",
                "tags": ["python", "fastapi", "mongodb", "beanie"],
                "location": "Google Meet"
            }
        }


# 2. Модель для частичного обновления (PUT)
class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Обновленное событие NoSQL (Буриков Алексей)",
                "location": "Hybrid"
            }
        }