from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field, field_validator


app = FastAPI(title="Task API", version="1.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return consistent JSON errors for HTTP exceptions."""
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

    model_config = {"extra": "forbid"}

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Title is required")

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Title is required")
            return value

        return value


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

    model_config = {"extra": "forbid"}

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Title is required")
            return value

        return value


# In-memory task storage for this simple demo application.
tasks: List[Task] = [
    Task(id=1, title="Write project proposal", done=False),
    Task(id=2, title="Buy groceries", done=True),
    Task(id=3, title="Call the dentist", done=False),
]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return friendly JSON errors for invalid request input."""
    for error in exc.errors():
        loc = error.get("loc", ())
        if "title" in loc:
            return JSONResponse(status_code=400, content={"error": "Title is required"})

    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


@app.get("/")
def read_root() -> dict[str, object]:
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate) -> Task:
    next_id = max((task.id for task in tasks), default=0) + 1
    new_task = Task(id=next_id, title=task_data.title, done=False)
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate) -> Task:
    for task in tasks:
        if task.id == task_id:
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.done is not None:
                task.done = task_data.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
