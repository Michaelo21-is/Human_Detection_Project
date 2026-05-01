
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Schema.AuthSchema import UserRegisterSchema, UserLoginSchema
from app.Services.AuthService import AuthService


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post("/register")
def register_user(
    user_data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    return AuthService.register_user(user_data, db)
@router.post("/login")
def login_user(
        user_data: UserLoginSchema,
        db: Session = Depends(get_db)
):
    return AuthService.login_user(user_data, db)