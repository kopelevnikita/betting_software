import logging

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.base import Base


_logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def create_multi(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, session: AsyncSession, record_id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == record_id)
        results = await session.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        skip=0,
        limit=100,
    ) -> List[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await session.execute(statement=statement)
        return results.scalars().all()

    async def create(self, session: AsyncSession, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def create_multi(self, session: AsyncSession, *, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        objs_in_data = [jsonable_encoder(obj) for obj in objs_in]
        db_objs = [self._model(**obj_in_data) for obj_in_data in objs_in_data]
        session.add_all(db_objs)
        await session.commit()
        for db_obj in db_objs:
            await session.refresh(db_obj)
        return db_objs

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)
        statement = update(self._model).where(self._model.id == db_obj.id).values(obj_in_data)
        await session.execute(statement=statement)
        await session.commit()
        return db_obj

    async def delete(self, session: AsyncSession, *, record_id: int) -> ModelType:
        db_obj = await session.get(self._model, record_id)
        statement = delete(self._model).where(self._model.id == record_id)
        await session.execute(statement=statement)
        await session.commit()
        return db_obj

    async def get_changed_fields(self, db_obj, obj_in: dict):
        """
        Method compare the fields of db_obj with obj_in and return the changed fields.
        """
        changed_fields = {}
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                current_value = getattr(db_obj, field)
                if current_value != value:
                    changed_fields[field] = {
                        "old": current_value,
                        "new": value,
                    }
        return changed_fields
