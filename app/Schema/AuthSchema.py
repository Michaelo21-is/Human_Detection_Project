from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
