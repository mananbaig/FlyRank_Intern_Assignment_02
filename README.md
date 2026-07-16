# Task Management API

A simple FastAPI CRUD API for managing tasks with an in-memory list.

## Features
- Create, read, update, and delete tasks
- In-memory storage only
- Automatic Swagger documentation
- Simple beginner-friendly structure

## Requirements
- Python 3.13
- FastAPI
- Uvicorn
- Pydantic

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:
- http://localhost:8000
- Swagger docs: http://localhost:8000/docs

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example curl commands

### Get API info
```bash
curl http://localhost:8000/
```

### Health check
```bash
curl http://localhost:8000/health
```

### List tasks
```bash
curl http://localhost:8000/tasks
```

### Create a task
```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

### Update a task
```bash
curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"done":true}'
```

### Delete a task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```
