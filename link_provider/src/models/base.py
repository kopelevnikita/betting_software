from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, declared_attr


class BaseField:

    @declared_attr
    def created_at(cls):
        """
        Method adds field 'created_at' for BaseField Model.
        """
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        """
        Method adds field 'updated_at' for BaseField Model.
        """
        return Column(DateTime, default=func.now(), onupdate=func.now())

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=BaseField)
