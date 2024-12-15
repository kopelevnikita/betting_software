from typing import Union, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.filter import Filter
from core.config import settings
from core.http_client import http_client
from schemas.event import EventSchemaCreate, EventSchemaUpdate
from models.event import Event as EventModel
from .base import RepositoryDB


class EventService(RepositoryDB[EventModel, EventSchemaCreate, EventSchemaUpdate]):

    async def get_filtered(
        self,
        session: AsyncSession,
        filter: list[dict] | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Method gets events by filter.
        """
        statement = select(self._model).offset(skip).limit(limit)
        if filter:
            filter = filter.dict(exclude_unset=True).get("filter", {})
            event_filter = Filter(self._model)
            conditions = event_filter.apply_filters(filter)
            if conditions is not None:
                statement = statement.where(conditions)
        result = await session.execute(statement)
        return result.scalars().all()

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: EventModel,
        obj_in: Union[EventSchemaUpdate, Dict[str, Any]]
    ) -> EventModel:
        """
        Method send request to update payout in bets.
        """
        client = http_client.get_client()
        changed_fields = await self.get_changed_fields(db_obj, obj_in)
        result = await super().update(
            session=session,
            db_obj=db_obj,
            obj_in=obj_in,
        )
        if "odds" in changed_fields:
            await client.post(
                url=f"{settings.bet_maker_url}/bets/recalculate_payout",
                json={
                    "event_id": db_obj.id,
                    "odds": float(db_obj.odds),
                }
            )
        if "status" in changed_fields:
            await client.post(
                url=f"{settings.bet_maker_url}/bets/calculate_bet",
                json={
                    "event_id": db_obj.id,
                    "odds": float(db_obj.odds),
                    "status": db_obj.status,
                }
            )
        return result


event_service = EventService(EventModel)
