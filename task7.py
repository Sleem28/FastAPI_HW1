"""
Создать RESTful API для управления списком задач. Приложение должно
использовать FastAPI и поддерживать следующие функции:
○ Получение списка всех задач.
○ Получение информации о задаче по её ID.
○ Добавление новой задачи.
○ Обновление информации о задаче по её ID.
○ Удаление задачи по её ID.
Каждая задача должна содержать следующие поля: ID (целое число),
Название (строка), Описание (строка), Статус (строка): "todo", "in progress",
"done".
"""
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Status:
    todo = "todo"
    in_progress = "in progress"
    done = "done"


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: Optional[str] = Status.todo


class ModTask(BaseModel):
    name: str
    description: Optional[str]
    status: Optional[str] = Status.todo


@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    task = [t for t in tasks if t.id == task.id]
    if task:
        return task[0]
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/create-task")
async def create_task(task: ModTask):
    cur_id = 1 if len(tasks) == 0 else max(tasks, key=lambda x: x.id).id + 1
    cur_task = Task(
        id=cur_id, name=task.name, description=task.description, status=task.status
    )
    tasks.append(cur_task)
    return "OK"


@app.put("/update/{task_id}")
async def change_task(task_id: int, task: ModTask):
    upd_task = [t for t in tasks if t.id == task_id]
    if not upd_task:
        raise HTTPException(status_code=404, detail="Task not found")
    upd_task[0].name = task.name
    upd_task[0].description = task.description
    upd_task[0].status = task.status
    return upd_task[0]


@app.delete("/remove/{task_id}")
async def remove_task_by_id(task_id: int):
    task = [t for t in tasks if t.id == task.id]
    if task:
        return tasks.remove(task[0])
    raise HTTPException(status_code=404, detail="Task not found")
