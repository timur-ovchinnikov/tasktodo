import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))  # Убедитесь, что путь к app правильный
from app.database import Base  # Теперь модуль доступен
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ToDo API is running!"}
