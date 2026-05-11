
from fastapi import APIRouter, Depends, Response
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
    response: Response,
    db: Session = Depends(get_db)
):
    session_id = AuthService.register_user(user_data, db)
    response.set_cookie(key="session_id", value=session_id)
@router.post("/login")
def login_user(
        user_data: UserLoginSchema,
        response: Response,
        db: Session = Depends(get_db)
):
    session_id = AuthService.login_user(user_data, db)
    response.set_cookie(key="session_id", value=session_id)