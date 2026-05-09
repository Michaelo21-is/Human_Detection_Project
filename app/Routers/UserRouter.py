from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.Services.UserService import UserService
router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)
@router.get("/is-user-logged-in")
def get_user(db: Session = Depends(get_db), session_id: str = Header(...)):
    return UserService.check_if_user_logged_in(db, session_id)