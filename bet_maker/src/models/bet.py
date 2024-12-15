import enum
from email.policy import default

from sqlalchemy import Column, Integer, DECIMAL, Enum

from .base import Base
from core.constants import MAX_DIGITS, DECIMAL_PLACES


class BetStatus(str, enum.Enum):
    NEW = "new"
    WON = "won"
    LOST = "lost"


class BetType(str, enum.Enum):
    WIN = "win"
    LOSE = "lose"


class Bet(Base):
    __tablename__ = "bet"

    event_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(MAX_DIGITS, DECIMAL_PLACES), nullable=False)
    payout = Column(DECIMAL(MAX_DIGITS, DECIMAL_PLACES), default=0.0, nullable=False)
    status = Column(Enum(BetStatus), default=BetStatus.NEW, nullable=False)
    bet_type = Column(Enum(BetType), nullable=False)
