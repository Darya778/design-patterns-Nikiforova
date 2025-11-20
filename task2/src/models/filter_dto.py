from dataclasses import dataclass
from typing import Any
from src.core.filters_enum import FilterType

@dataclass
class FilterDTO:
    field_name: str
    value: Any
    filter_type: FilterType

    @staticmethod
    def from_dict(data: dict):
        """
        Безопасно создает FilterDTO.
        Поддерживает строковые значения filter_type ('LIKE', 'EQUALS').
        """
        if not isinstance(data, dict):
            raise ValueError("Filter must be an object")

        field = data.get("field_name")
        value = data.get("value")
        ftype = data.get("filter_type")

        if field is None:
            raise ValueError("Missing field 'field_name'")
        if value is None:
            raise ValueError("Missing field 'value'")
        if ftype is None:
            raise ValueError("Missing field 'filter_type'")

        if isinstance(ftype, str):
            ftype_norm = ftype.strip().upper()
            try:
                ftype_enum = FilterType[ftype_norm]
            except KeyError:
                raise ValueError(f"Invalid filter_type '{ftype}'")
        elif isinstance(ftype, FilterType):
            ftype_enum = ftype
        else:
            raise ValueError(f"Invalid filter_type '{ftype}'")

        return FilterDTO(
            field_name=field,
            value=value,
            filter_type=ftype_enum
        )
