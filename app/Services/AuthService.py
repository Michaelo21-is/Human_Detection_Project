import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Models.UsersModel import User
from app.Schema.RegisterUserSchema import UserRegisterSchema
class AuthService:
    @staticmethod
    def register_user(user_data: UserRegisterSchema, db: Session):
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(
            name=user_data.firstName,
            email=user_data.email,
            password=user_data.password,
            last_name=user_data.lastName,
            session_id=str(uuid.uuid4())
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user.session_id

