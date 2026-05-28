from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Models.UsersModel import User
class UserService:
    def check_if_user_logged_in(db: Session, session_id: str):
        user = db.query(User).filter(User.session_id == session_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user.voice_preference
    def set_voice_preference(db: Session, session_id: str, voice_id: str):
        updated_rows = (
            db.query(User)
            .filter(User.session_id == session_id)
            .update(
                {User.voice_preference: voice_id},
                synchronize_session=False
            )
        )

        if updated_rows == 0:
            raise HTTPException(status_code=401, detail="User not found")

        db.commit()
        return "user update successfully voice preference"