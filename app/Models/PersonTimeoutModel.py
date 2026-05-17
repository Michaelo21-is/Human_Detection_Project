from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class PersonTimeout(Base):
    __tablename__ = "person_timeout"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    recognized_person_id = Column(
        Integer,
        ForeignKey("recognized_people.id"),
        nullable=False,
        unique=True
    )

    last_spoken_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    recognized_person = relationship(
        "RecognizedPeople",
        back_populates="person_timeout"
    )