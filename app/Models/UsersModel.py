from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    voice_preference = Column(String, nullable=False)
    session_id = Column(String, nullable=False)

    recognized_people_mappings = relationship(
        "UsersRecognizedPeopleMapper",
        back_populates="user"
    )