from sqlalchemy import Column, Integer
from app.database import Base

class UsersRecognizedPeopleMapper(Base):
    __tablename__ = 'user_recognized_people_mapping'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    recognized_people_id = Column(Integer, nullable=False)