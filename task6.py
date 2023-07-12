"""
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


@app.get("/users", response_class=HTMLResponse)
async def get_all_users(request: Request):
    context = {
        "text": "TEXT",
        "title": "USERS INFO",
        "users": users,
    }
    return templates.TemplateResponse("users.html", {"request": request, **context})


@app.get("/add-user", response_class=HTMLResponse)
async def add_user(request: Request):
    context = {
        "title": "ADD NEW USER",
    }
    return templates.TemplateResponse("add-user.html", {"request": request, **context})


@app.post("/save_user", response_class=HTMLResponse)
def save_user(request: Request, username=Form(), email=Form(), password=Form()):
    user_id = len(users) + 1
    users.append(User(id=user_id, name=username, email=email, password=password))
    context = {
        "title": "USER ADDED",
    }
    return templates.TemplateResponse(
        "user_added.html", {"request": request, **context}
    )
