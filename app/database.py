from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Замените DATABASE_URL на ваш реальный URL
DATABASE_URL = "postgresql://todo_user:todo_password@db/todo_db"

# Создание двигателя (engine) для подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Базовый класс для моделей
Base = declarative_base()

# Создание сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
