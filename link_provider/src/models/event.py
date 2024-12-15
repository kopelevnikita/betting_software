import enum

from sqlalchemy import Column, String, DECIMAL, DateTime, Enum

from .base import Base
from core.constants import MAX_DIGITS, DECIMAL_PLACES


class EventStatus(str, enum.Enum):
    NEW = "new"
    WON = "won"
    LOST = "lost"


class Event(Base):
    __tablename__ = "event"

    team1 = Column(String, nullable=False)
    team2 = Column(String, nullable=False)
    odds = Column(DECIMAL(MAX_DIGITS, DECIMAL_PLACES), nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.NEW, nullable=False)
