import logging
from datetime import datetime, timezone

from fastapi import status, HTTPException

from core.config import settings
from core.http_client import http_client
from db import redis
from schemas import event as event_schema

from .cache_service import RedisService


_logger = logging.getLogger(__name__)


class EventService:

    async def get_event_by_id(
        self,
        event_id: int,
    ) -> event_schema.EventSchemaDisplay:
        """
        Method get event by id.
        """
        client = http_client.get_client()
        redis_service = RedisService(redis.redis)
        event_data = await redis_service.get_value(f"event_{event_id}")
        if not event_data:
            _logger.debug(f"{settings.link_provider_url}/events/event/{event_id}")
            response = await client.get(
                url=f"{settings.link_provider_url}/events/event/{event_id}",
            )
            if getattr(response, "status_code", False) == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {event_id} not found!")
            elif getattr(response, "status_code", False) != 200:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request!")
            event_data = response.json()
            await RedisService(redis.redis).set_value(f"event_{event_id}", event_data)
        return event_data

    async def get_events(
        self,
    ) -> list[event_schema.EventSchemaDisplay]:
        """
        Method get all events by filter.
        """
        client = http_client.get_client()
        redis_service = RedisService(redis.redis)
        events_data = await redis_service.get_value("events")
        current_time = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="milliseconds")
        if not events_data:
            _logger.debug(f"{settings.link_provider_url}/events/events/filter")
            response = await client.post(
                url=f"{settings.link_provider_url}/events/events/filter",
                json={
                    "filter": [
                        {
                            "field": "deadline",
                            "operator": ">",
                            "value": current_time,
                        },
                        {
                            "field": "status",
                            "operator": "==",
                            "value": "new",
                        },
                    ]
                }
            )
            if getattr(response, "status_code", False) != 200:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request!")
            events_data = response.json()
            await RedisService(redis.redis).set_value("events", events_data)
        return events_data


event_service = EventService()
