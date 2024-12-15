from datetime import datetime
from typing import Type, TypeVar, Union

from sqlalchemy import and_, or_

from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class Filter:

    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    def apply_filters(self, filters: list[dict]) -> Union[None, and_]:
        """
        Method compose filters.
        """
        conditions = []
        for filter_ in filters:
            field = getattr(self._model, filter_["field"], None)
            if field is None:
                raise ValueError(f"Field '{filter_['field']}' not found in model {self._model.__name__}.")
            op = filter_["operator"]
            value = filter_["value"]
            if isinstance(value, str) and field.type.python_type is datetime:
                value = datetime.fromisoformat(value)
            if op == "==":
                conditions.append(field == value)
            elif op == "!=":
                conditions.append(field != value)
            elif op == ">":
                conditions.append(field > value)
            elif op == "<":
                conditions.append(field < value)
            elif op == ">=":
                conditions.append(field >= value)
            elif op == "<=":
                conditions.append(field <= value)
            elif op == "in":
                conditions.append(field.in_(value))
            elif op == "not_in":
                conditions.append(~field.in_(value))
            elif op == "like":
                conditions.append(field.like(value))
            elif op == "ilike":
                conditions.append(field.ilike(value))
            elif op == "or":
                conditions.append(or_(*[getattr(self._model, cond["field"]) == cond["value"] for cond in value]))
            elif op == "and":
                conditions.append(and_(*[getattr(self._model, cond["field"]) == cond["value"] for cond in value]))
            else:
                raise ValueError(f"Unsupported operator '{op}'.")
        return and_(*conditions) if conditions else None
