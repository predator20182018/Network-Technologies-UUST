from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "email": "burikov@packt.com",
                "password": "strongpassword123!",
                "events": []
            }
        }


class NewUser(User):
    pass


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "burikov@packt.com",
                "password": "strongpassword123!"
            }
        }