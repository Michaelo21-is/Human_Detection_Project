from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.Services.UserService import UserService
router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)
@router.get("/is-user-logged-in")
def get_user(db: Session = Depends(get_db), request: Request = Request):
    session_id = request.cookies.get("session_id")
    return UserService.check_if_user_logged_in(db, session_id)