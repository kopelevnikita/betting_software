from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.constants import DECIMAL_PLACES
from models.bet import Bet as BetModel
from schemas.bet import BetSchemaCreate, BetSchemaUpdate
from schemas.event import EventRecalculateSchema, EventCalculateSchema

from .base import RepositoryDB
from .event import event_service


class BetService(RepositoryDB[BetModel, BetSchemaCreate, BetSchemaUpdate]):

    async def create(
        self,
        session: AsyncSession,
        obj_in: BetSchemaCreate,
    ) -> BetModel:
        """
        Method creates new bet and check event.
        """
        if isinstance(obj_in, dict):
            input_data = obj_in
        else:
            input_data = obj_in.dict(exclude_unset=True)
        event_data = await event_service.get_event_by_id(input_data.get("event_id"))
        deadline = datetime.fromisoformat(event_data.get("deadline")).replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        if current_time >= deadline:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deadline for placing bet on this event has passed."
            )
        if event_data.get("status") != "new":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The event has already played."
            )
        new_bet = await super().create(
            session=session,
            obj_in=obj_in,
        )
        odds = Decimal(event_data.get("odds", 1)).quantize(Decimal(f"0.{''.zfill(DECIMAL_PLACES)}"), rounding=ROUND_HALF_UP)
        payout = new_bet.amount * odds
        new_bet.payout = payout
        session.add(new_bet)
        await session.commit()
        await session.refresh(new_bet)
        return new_bet

    async def _get_bets(
        self,
        session: AsyncSession,
        event_id: int,
    ) -> list[BetModel]:
        """
        Method gets bets by event_id.
        """
        statement = select(self._model).where(self._model.event_id == event_id)
        results = await session.execute(statement=statement)
        return results.scalars().all()

    async def recalculate_bets(
        self,
        session: AsyncSession,
        event_data: EventRecalculateSchema,
    ) -> list[BetModel]:
        """
        Method recalculates bets if changed odds in related events.
        """
        event_data = jsonable_encoder(event_data)
        new_odds = Decimal(event_data.get("odds", 1)).quantize(
            Decimal(f"0.{''.zfill(DECIMAL_PLACES)}"), rounding=ROUND_HALF_UP
        )
        bets = await self._get_bets(
            session=session,
            event_id=event_data.get("event_id"),
        )
        for bet in bets:
            bet.payout = bet.amount * new_odds
            session.add(bet)
            await session.commit()
            await session.refresh(bet)
        return bets

    async def calculate_bets(
        self,
        session: AsyncSession,
        event_data: EventCalculateSchema,
    ) -> list[BetModel]:
        """
        Method recalculates bets and changed status if changed status in related events.
        """
        event_data = jsonable_encoder(event_data)
        new_odds = Decimal(event_data.get("odds", 1)).quantize(
            Decimal(f"0.{''.zfill(DECIMAL_PLACES)}"), rounding=ROUND_HALF_UP
        )
        bets = await self._get_bets(
            session=session,
            event_id=event_data.get("event_id"),
        )
        for bet in bets:
            self.update_bet_status_and_payout(bet, event_data.get("status"), new_odds)
            session.add(bet)
        await session.commit()
        await session.refresh(bets)
        return bets

    def update_bet_status_and_payout(
        self,
        bet: BetModel,
        event_status: str,
        new_odds: Decimal,
    ) -> None:
        """
        Method update bet status and payout based on event status and bet type.
        """
        status_payout_mapping = {
            ("win", "won"): {"status": "won", "payout": bet.amount * new_odds},
            ("win", "lost"): {"status": "lost", "payout": Decimal(0)},
            ("lose", "won"): {"status": "lost", "payout": Decimal(0)},
            ("lose", "lost"): {"status": "won", "payout": bet.amount * new_odds},
        }
        result = status_payout_mapping.get(
            (bet.bet_type, event_status),
            {"status": "new", "payout": bet.amount * new_odds}
        )
        bet.status = result["status"]
        bet.payout = result["payout"]


bet_service = BetService(BetModel)
