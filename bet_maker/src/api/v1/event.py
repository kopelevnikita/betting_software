import logging

from fastapi import APIRouter, status, Depends, HTTPException, Path

from schemas import event as event_schema
from services.event import event_service


_logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/events",
    status_code=status.HTTP_200_OK,
    summary="Get all events",
    description="Get all events",
    response_model=list[event_schema.EventSchemaDisplay],
)
async def get_events() -> list[event_schema.EventSchemaDisplay]:
    events = await event_service.get_events()
    if not events:
        _logger.warning("Events not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Events not found!",
        )
    return events
