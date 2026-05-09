from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Models.UsersModel import User
class UserService:
    def check_if_user_logged_in(db: Session, session_id: str):
        user = db.query(User).filter(User.session_id == session_id).first()
        if not User:
            raise HTTPException(status_code=401, detail="User not found")
        return "user is logged in"