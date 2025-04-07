from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.security import create_access_token
from app.crud import verify_user_password  # Updated import

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.Login, db: Session = Depends(get_db)):
    user = verify_user_password(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}