from fastapi import APIRouter, Path
from model import Todo

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Задача успешно добавлена студентом: Буриков Алексей"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todos": todo_list}


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    todo_id: int = Path(..., title="ID задачи, которую нужно получить")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": "Задача с указанным ID не найдена."}

@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: Todo,
    todo_id: int = Path(..., title="ID задачи для обновления")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {"message": "Задача успешно обновлена студентом: Буриков Алексей"}
    return {"message": "Задача с указанным ID не найдена."}


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(
    todo_id: int = Path(..., title="ID задачи для удаления")
) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": "Задача успешно удалена студентом: Буриков Алексей"}
    return {"message": "Задача с указанным ID не найдена."}