from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from contextlib import asynccontextmanager
import uvicorn

from database.connection import Settings
from models.events import Event
from models.users import User
from routes.users import user_router
from routes.events import event_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация асинхронного драйвера Beanie + MongoDB при старте
    await settings.initialize_database()
    yield


app = FastAPI(
    title="Event Planner API (MongoDB + Beanie)",
    description="Практическая работа: Подключение к нереляционной БД MongoDB. Выполнил: Буриков Алексей",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")


# 🛠 Асинхронная панель администратора для инспекции коллекций MongoDB
@app.get("/admin", response_class=HTMLResponse, tags=["Администрирование"])
async def admin_dashboard():
    # 1. Асинхронная выгрузка документов из коллекций MongoDB
    events = await Event.find_all().to_list()
    users = await User.find_all().to_list()

    # Формирование строк коллекции events
    event_rows = ""
    for e in events:
        tags_badges = "".join([f"<span class='badge bg-secondary me-1'>{t}</span>" for t in (e.tags or [])])
        event_rows += f"""
        <tr>
            <td><code class="text-primary fw-bold">{str(e.id)}</code></td>
            <td><b>{e.title}</b></td>
            <td><span class="badge bg-info text-dark">{e.location}</span></td>
            <td><small class="text-muted">{e.description}</small></td>
            <td>{tags_badges}</td>
        </tr>
        """
    if not event_rows:
        event_rows = "<tr><td colspan='5' class='text-center text-muted p-4'>Коллекция 'events' пока пуста. Создайте документ через POST /event/new</td></tr>"

    # Формирование строк коллекции users
    user_rows = ""
    for u in users:
        user_rows += f"""
        <tr>
            <td><code class="text-primary fw-bold">{str(u.id)}</code></td>
            <td><b>{u.email}</b></td>
            <td><code>{u.password[:3]}*****</code></td>
            <td><span class="badge bg-secondary">{len(u.events or [])} связей</span></td>
        </tr>
        """
    if not user_rows:
        user_rows = "<tr><td colspan='4' class='text-center text-muted p-4'>Коллекция 'users' пока пуста. Зарегистрируйте пользователя через POST /user/signup</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>MongoDB Admin Dashboard — Буриков Алексей</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="bg-light p-4">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <div>
                    <h2>🍃 Панель управления MongoDB (Beanie ODM)</h2>
                    <span class="text-muted">
                        СУБД: <b>MongoDB (порт 27017, база 'planner')</b> | 
                        Разработчик: <b>Буриков Алексей</b>
                    </span>
                </div>
                <div>
                    <button onclick="location.reload()" class="btn btn-outline-dark me-2">🔄 Обновить</button>
                    <a href="/docs" class="btn btn-primary">Swagger UI</a>
                </div>
            </div>

            <!-- Коллекция 1: events -->
            <div class="card shadow-sm mb-4 border-0">
                <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center py-2">
                    <span>📁 Коллекция: <code>events</code> (Документы BSON)</span>
                    <span class="badge bg-success">Документов: {len(events)}</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 align-middle">
                        <thead class="table-secondary">
                            <tr>
                                <th style="width: 25%;">ObjectId (_id)</th>
                                <th style="width: 25%;">Название (Title)</th>
                                <th style="width: 15%;">Локация</th>
                                <th style="width: 20%;">Описание</th>
                                <th style="width: 15%;">Теги (Array)</th>
                            </tr>
                        </thead>
                        <tbody>{event_rows}</tbody>
                    </table>
                </div>
            </div>

            <!-- Коллекция 2: users -->
            <div class="card shadow-sm border-0">
                <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center py-2">
                    <span>👤 Коллекция: <code>users</code></span>
                    <span class="badge bg-warning text-dark">Документов: {len(users)}</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 align-middle">
                        <thead class="table-secondary">
                            <tr>
                                <th style="width: 25%;">ObjectId (_id)</th>
                                <th style="width: 35%;">Email</th>
                                <th style="width: 25%;">Хэш пароля</th>
                                <th style="width: 15%;">События</th>
                            </tr>
                        </thead>
                        <tbody>{user_rows}</tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)