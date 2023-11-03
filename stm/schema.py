from __future__ import annotations

from typing import Any
from pydantic import BaseModel, create_model
from typing import Any
from pendulum.datetime import DateTime


# todo.maybe: submit pull request to pydantic with add feature


class PendulumDateTime(DateTime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> DateTime:
        if isinstance(v, DateTime):
            return v
        if isinstance(v, str):
            return cls.parse(v)
        raise ValueError("not a valid datetime")

    @classmethod
    def parse(cls, v: str) -> PendulumDateTime:
        raise NotImplemented

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
