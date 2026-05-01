
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Schema.RegisterUserSchema import UserRegisterSchema
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