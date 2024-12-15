import logging

from fastapi import APIRouter, status, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas import bet as bet_schema
from schemas import event as event_schema
from services.bet import bet_service

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/bets",
    status_code=status.HTTP_200_OK,
    summary="Get all bets",
    description="Get all bets",
    response_model=list[bet_schema.BetSchemaDisplay],
)
async def get_bets(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> list[bet_schema.BetSchemaDisplay]:
    """
    Get all bets.
    """
    bets = await bet_service.get_multi(
        session=session,
        skip=skip,
        limit=limit,
    )
    if not bets:
        _logger.warning("Bets not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bets not found!",
        )
    return bets


@router.post(
    "/bet",
    status_code=status.HTTP_200_OK,
    summary="Place a bet",
    description="Place a bet",
    response_model=bet_schema.BetSchemaDisplay,
)
async def place_bet(
    input_data: bet_schema.BetSchemaCreate,
    session: AsyncSession = Depends(get_session),
) -> bet_schema.BetSchemaDisplay:
    """
    Place a bet.
    """
    bet = await bet_service.create(
        session=session,
        obj_in=input_data,
    )
    return bet


@router.post(
    "/recalculate_payout",
    status_code=status.HTTP_200_OK,
    summary="Recalculate payout when changing odds in related events",
    description="Recalculate payout when changing odds in related events",
    response_model=list[bet_schema.BetSchemaDisplay],
)
async def recalculate_payout(
    event_data: event_schema.EventRecalculateSchema = Body(...),
    session: AsyncSession = Depends(get_session),
) -> list[bet_schema.BetSchemaDisplay]:
    """
    Recalculate payout for bets when changing odds in related events.
    """
    bets = await bet_service.recalculate_bets(
        session=session,
        event_data=event_data,
    )
    return bets


@router.post(
    "/calculate_bet",
    status_code=status.HTTP_200_OK,
    summary="Calculate bet when changing status in related events",
    description="Recalculate payout when changing odds in related events",
    response_model=list[bet_schema.BetSchemaDisplay],
)
async def calculate_bet(
    event_data: event_schema.EventCalculateSchema = Body(...),
    session: AsyncSession = Depends(get_session),
) -> list[bet_schema.BetSchemaDisplay]:
    """
    Calculate payout for bets when changing status in related events.
    """
    bets = await bet_service.calculate_bets(
        session=session,
        event_data=event_data,
    )
    return bets
