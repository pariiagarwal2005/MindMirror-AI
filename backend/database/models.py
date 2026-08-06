from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base
from datetime import datetime


class Journal(Base):

    __tablename__ = "journals"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    text = Column(
        String
    )


    mood = Column(
        String,
        nullable=True
    )


    emotion = Column(
        String,
        nullable=True
    )


    confidence = Column(
        String,
        nullable=True
    )


    ai_reflection = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )