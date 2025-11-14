from dataclasses import dataclass
from typing import List
from src.core.filters_enum import FilterType

"""DTO для передачи параметров фильтрации"""
@dataclass
class FilterDTO:
    field_name: str
    value: str
    filter_type: FilterType
