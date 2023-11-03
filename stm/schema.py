from __future__ import annotations

import pendulum
from pendulum.datetime import DateTime
from datetime import datetime
from typing import Any, Union
from pydantic import BaseModel


# todo.maybe: submit pull request to pydantic with add feature
# * or sep into new mini package


class PendulumDateTime(DateTime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, int, float, datetime, DateTime]) -> DateTime:
        try:
            return cls.parse(v)
        except ValueError:
            raise ValueError("not a valid datetime")

    @classmethod
    def parse(cls, v: Union[str, int, float, datetime, DateTime]) -> PendulumDateTime:
        if isinstance(v, DateTime):
            return v
        if isinstance(v, int) or isinstance(v, float):
            return pendulum.from_timestamp(v)
        if isinstance(v, datetime):
            return pendulum.from_timestamp(v.timestamp())
        if isinstance(v, str):
            return pendulum.parse(v)
        raise ValueError("could not parse")

    @classmethod
    def __get_pydantic_core_schema__(cls, annotations: Any) -> dict:
        return {
            "title": "PendulumDateTime",
            "type": "string",
            "format": "date-time",
        }


# Now use PendulumDateTime in your model.
class MyModel(BaseModel):
    created_at: PendulumDateTime
