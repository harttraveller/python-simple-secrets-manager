from __future__ import annotations

import pendulum
from pendulum.datetime import DateTime
from typing import Any
from typing_extensions import Annotated
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

# ref: https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types


class _PendulumDateTime(DateTime):
    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate

    # @classmethod
    # def validate(cls, v: Union[str, int, float, datetime, DateTime]) -> DateTime:
    #     try:
    #         return cls.parse(v)
    #     except ValueError:
    #         raise ValueError("not a valid datetime")

    # @classmethod
    # def parse(cls, v: Union[str, int, float, datetime, DateTime]) -> PendulumDateTime:
    #     if isinstance(v, DateTime):
    #         return v
    #     if isinstance(v, int) or isinstance(v, float):
    #         return pendulum.from_timestamp(v)
    #     if isinstance(v, datetime):
    #         return pendulum.from_timestamp(v.timestamp())
    #     if isinstance(v, str):
    #         return pendulum.parse(v)
    #     raise ValueError("could not parse")

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_str(value: str) -> DateTime:
            return pendulum.parse(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(DateTime),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.int_schema())


# We now create an `Annotated` wrapper that we'll use as the annotation for fields on `BaseModel`s, etc.
PendulumDatetime = Annotated[DateTime, _PendulumDateTime]

# todo.maybe: submit pull request to pydantic with add feature
# * or sep into new mini package
