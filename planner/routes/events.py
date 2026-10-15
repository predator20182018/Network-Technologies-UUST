from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

event_router = APIRouter(tags=["Events"])

# Временная база данных событий в памяти
events = []


# Получить все события
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


# Получить одно событие по ID
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным ID не найдено"
    )


# Создать новое событие с проверкой уникальности ID
@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    for event in events:
        if event.id == body.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Событие с ID {body.id} уже существует (Буриков Алексей)"
            )
    events.append(body)
    return {"message": "Событие успешно создано (Буриков Алексей)"}

# Удалить событие по ID
@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Событие успешно удалено"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным ID не найдено"
    )


# Удалить все события
@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Все события успешно удалены"}