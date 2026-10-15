from pydantic import BaseModel
from typing import List


class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch (Буриков Алексей)",
                "image": "https://linktomyimage.com/image.png",
                "description": "Презентация и обсуждение книги по FastAPI",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }