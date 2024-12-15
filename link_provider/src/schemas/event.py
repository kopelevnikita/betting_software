from datetime import datetime

from pydantic import BaseModel, Field, condecimal

from .base import BaseSchema
from core.constants import MAX_DIGITS, DECIMAL_PLACES
from models.event import EventStatus


class EventSchema(BaseModel):
    odds: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=2.0)
    deadline: datetime = Field(..., example="2025-01-01T18:00:00")
    status: EventStatus = Field(default=EventStatus.NEW)

    class Config:
        orm_mode = True


class EventSchemaCreate(EventSchema):
    team1: str
    team2: str

    class Config:
        json_encoders = {
            datetime: lambda d: d
        }


class EventSchemaUpdate(EventSchema):
    ...


class EventSchemaDisplay(BaseSchema, EventSchema):
    team1: str
    team2: str
