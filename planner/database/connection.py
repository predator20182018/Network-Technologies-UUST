from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Any, List, Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017/planner"

    async def initialize_database(self):
        from models.events import Event
        from models.users import User

        client = AsyncIOMotorClient(self.DATABASE_URL)
        # Явный выбор базы данных из клиента
        db = client["planner"]
        await init_beanie(
            database=db,
            document_models=[Event, User]
        )


# Универсальный класс CRUD для работы с коллекциями Beanie
class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.model_dump() if hasattr(body, "model_dump") else body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True