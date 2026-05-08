from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UsersRecognizedPeopleMapper(Base):
    __tablename__ = "user_recognized_people_mapping"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recognized_people_id = Column(Integer, ForeignKey("recognized_people.id"), nullable=False)

    user = relationship(
        "User",
        back_populates="recognized_people_mappings"
    )

    recognized_people = relationship(
        "RecognizedPeople",
        back_populates="user_mappings"
    )