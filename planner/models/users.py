from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]] = []

    class Settings:
        name = "users"  # Имя коллекции в MongoDB

    class Config:
        json_schema_extra = {
            "example": {
                "email": "burikov@packt.com",
                "password": "StrongPassword123!",
                "events": []
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "burikov@packt.com",
                "password": "StrongPassword123!"
            }
        }