
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.Schema.AuthSchema import UserRegisterSchema, UserLoginSchema
from app.Services.AuthService import AuthService
import os

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

SECURE = os.getenv("SECURE", "False").lower() == "true"

@router.post("/register")
def register_user(
    user_data: UserRegisterSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    session_id = AuthService.register_user(user_data, db)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=SECURE,
        samesite="none",
        path="/",
        max_age=60 * 60 * 24 * 7,
    )
    return {"message": "registered successfully"}
@router.post("/login")
def login_user(
        user_data: UserLoginSchema,
        response: Response,
        db: Session = Depends(get_db)
):
    session_id = AuthService.login_user(user_data, db)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=SECURE,
        samesite="none",
        path="/",
        max_age=60 * 60 * 24 * 7,
    )