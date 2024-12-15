from pydantic import BaseModel, Field, condecimal

from .base import BaseSchema
from core.constants import MAX_DIGITS, DECIMAL_PLACES
from models.bet import BetStatus, BetType


class BetSchema(BaseModel):
    status: BetStatus = Field(default=BetStatus.NEW)
    bet_type: BetType = Field(default=BetType.WIN)

    class Config:
        orm_mode = True


class BetSchemaCreate(BetSchema):
    event_id: int
    amount: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=100.00)


class BetSchemaUpdate(BetSchema):
    payout: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=200.00)


class BetSchemaDisplay(BaseSchema, BetSchema):
    event_id: int
    amount: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=100.00)
    payout: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=200.00)
