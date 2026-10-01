from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []


# 1. Добавление задачи со статусом 201 Created
@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Задача успешно добавлена студентом: Буриков Алексей"}


# 2. Получение списка с фильтрацией через response_model (без id)
@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
    return {"todos": todo_list}


# 3. Получение конкретной задачи по ID с выбросом 404 ошибки
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    todo_id: int = Path(..., title="ID задачи для получения")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не найдена (Буриков Алексей)"
    )


# 4. Обновление задачи (PUT) с выбросом 404 ошибки
@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="ID задачи для обновления")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {"message": "Задача успешно обновлена студентом: Буриков Алексей"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача для обновления не найдена (Буриков Алексей)"
    )


# 5. Удаление одной задачи по ID с выбросом 404 ошибки
@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(
    todo_id: int = Path(..., title="ID задачи для удаления")
) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": "Задача успешно удалена студентом: Буриков Алексей"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача для удаления не найдена (Буриков Алексей)"
    )


# 6. Очистить все задачи
@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {"message": "Все задачи успешно удалены студентом: Буриков Алексей"}