from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, condecimal

from .base import BaseSchema
from core.constants import MAX_DIGITS, DECIMAL_PLACES


class EventStatus(str, Enum):
    NEW = "new"
    WON = "won"
    LOST = "lost"


class EventSchema(BaseModel):
    odds: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=2.0)
    deadline: datetime = Field(..., example="2025-01-01T18:00:00")
    status: EventStatus = Field(default=EventStatus.NEW)


class EventSchemaDisplay(BaseSchema, EventSchema):
    ...


class EventRecalculateSchema(BaseModel):
    event_id: int = Field(..., example="1")
    odds: condecimal(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) = Field(..., example=2.0)


class EventCalculateSchema(EventRecalculateSchema):
    status: EventStatus = Field(default=EventStatus.NEW)
