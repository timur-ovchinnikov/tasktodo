import sys
import os
from fastapi import FastAPI, HTTPException
from app.models import User
from app.schemas import UserCreate
from app.database import SessionLocal
from app.crud import create_user  # Функция, которая будет создавать пользователя

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ToDo API is running!"}

@app.post("/register")
async def register_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = create_user(db, user)
        return {"msg": "User created", "user": db_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating user: " + str(e))
