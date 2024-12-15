from pydantic import BaseModel
from typing import Union, Literal


class FilterSchema(BaseModel):
    field: str
    operator: Literal["==", "!=", ">", "<", ">=", "<=", "in", "not_in", "like", "ilike", "or", "and"]
    value: Union[str, int, float, bool]


class FiltersRequest(BaseModel):
    filter: list[FilterSchema] | None

    class Config:
        schema_extra = {
            "example": {
                "filter": [
                    {
                        "field": "deadline",
                        "operator": ">",
                        "value": "2024-12-14T13:37:34.691",
                    }
                ]
            }
        }