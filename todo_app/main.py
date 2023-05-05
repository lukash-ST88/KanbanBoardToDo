from fastapi import FastAPI

app = FastAPI(
    title='ToDoApp'
)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]
