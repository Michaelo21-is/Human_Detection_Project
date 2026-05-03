from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


class RecognizedPeople(Base):
    __tablename__ = "recognized_people"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    where_is_known_from = Column(String, nullable=False)
    image_location = Column(String, nullable=False)

    re