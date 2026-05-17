import uuid

from fastapi import HTTPException
from app.core.password_encoder import encode_password, verify_password
from app.Models.UsersModel import User
from sqlalchemy.orm import Session
from app.Schema.AuthSchema import UserRegisterSchema, UserLoginSchema
class AuthService:
    @staticmethod
    def register_user(user_data: UserRegisterSchema, db: Session):
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        encoded_password = encode_password(user_data.password)
        new_user = User(
            name=user_data.firstName,
            email=user_data.email,
            password=encoded_password,
            last_name=user_data.lastName,
            session_id=str(uuid.uuid4())
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user.session_id
    @staticmethod
    def login_user(user_data: UserLoginSchema, db: Session):
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            if verify_password(user_data.password, existing_user.password):
                return existing_user.session_id
            raise HTTPException(status_code=401, detail="Incorrect password")
        raise HTTPException(status_code=401, detail="Incorrect email")

