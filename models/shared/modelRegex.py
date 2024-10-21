import re
from dataclasses import dataclass
from typing import Any

from pydantic_core import CoreSchema, PydanticCustomError, core_schema

from pydantic import (
    GetCoreSchemaHandler,
    GetJsonSchemaHandler
)
from pydantic.json_schema import JsonSchemaValue


@dataclass
class MsRegex:
    pattern: str

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        regex = re.compile(self.pattern)

        def match(v: str) -> str:
            if not regex.match(v):
                raise PydanticCustomError(
                    'string_pattern_mismatch',
                    "String should match pattern '{pattern}'",
                    {'pattern': self.pattern},
                )
            return v

        return core_schema.no_info_after_validator_function(
            match,
            handler(source_type),
        )

    def __get_pydantic_json_schema__(
        self, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema['pattern'] = self.pattern
        return json_schema