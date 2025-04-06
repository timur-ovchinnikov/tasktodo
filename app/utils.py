from datetime import datetime, timedelta
from typing import Optional

import jwt
from app.schemas import User
from app.models import User as UserModel
from app.core.config import SECRET_KEY, ALGORITHM  # Переменные для конфигурации

# Время жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Генерация JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверка токена и извлечение данных
def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError:
        raise Exception("Token is invalid")
