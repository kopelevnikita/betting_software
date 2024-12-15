import logging

from fastapi import APIRouter, status, Depends, HTTPException, Path, Body

from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas import event as event_schema, filter as filter_schema
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
async def get_events(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> list[event_schema.EventSchemaDisplay]:
    """
    Get all events.
    """
    events = await event_service.get_multi(
        session=session,
        skip=skip,
        limit=limit,
    )
    if not events:
        _logger.warning("Events not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Events not found!",
        )
    return events


@router.get(
    "/event/{event_id}",
    status_code=status.HTTP_200_OK,
    summary="Get event by event_id",
    description="Get event by event_id",
    response_model=event_schema.EventSchemaDisplay,
)
async def get_event(
    *,
    session: AsyncSession = Depends(get_session),
    event_id: int = Path(..., description="Event ID"),
) -> event_schema.EventSchemaDisplay:
    """
    Get event by event_id.
    """
    event = await event_service.get(
        session=session,
        record_id=event_id,
    )
    if not event:
        _logger.warning("Event not found by event_id: %s.", event_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found!",
        )
    return event


@router.post(
    "/events/filter",
    status_code=status.HTTP_200_OK,
    summary="Get all events by filter",
    description="Get all events by filter",
    response_model=list[event_schema.EventSchemaDisplay],
)
async def get_filtered_events(
    filter: filter_schema.FiltersRequest = Body(...),
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> list[event_schema.EventSchemaDisplay]:
    """
    Get all events by filter.
    """
    events = await event_service.get_filtered(
        filter=filter,
        session=session,
        skip=skip,
        limit=limit,
    )
    if not events:
        _logger.warning("Events not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Events not found!",
        )
    return events


@router.put(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
    summary="Change values in event",
    description="Change values in event",
    response_model=event_schema.EventSchemaDisplay,
)
async def update_event(
    *,
    session: AsyncSession = Depends(get_session),
    event_id: int = Path(..., description="Event ID"),
    input_data: event_schema.EventSchemaUpdate,
) -> event_schema.EventSchemaDisplay:
    """
    Change values in event.
    """
    event = await event_service.get(
        session=session,
        record_id=event_id,
    )
    if not event:
        _logger.warning("Event not found by event_id: %s.", event_id)
        raise HTTPException(
            status_code=404,
            detail="Event not found!",
        )
    updated_event = await event_service.update(
        session=session,
        db_obj=event,
        obj_in=input_data.dict(),
    )
    return updated_event


@router.post(
    "/event/create",
    status_code=status.HTTP_200_OK,
    summary="Create a new event",
    description="Create a new event",
    response_model=event_schema.EventSchemaDisplay,
)
async def create_event(
    input_data: event_schema.EventSchemaCreate,
    session: AsyncSession = Depends(get_session),
) -> event_schema.EventSchemaDisplay:
    """
    Create a new event.
    """
    event = await event_service.create(
        session=session,
        obj_in=input_data,
    )
    return event

