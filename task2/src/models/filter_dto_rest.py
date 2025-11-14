from pydantic import BaseModel
from enum import Enum

"""Типы фильтров для REST API"""
class FilterTypeEnum(str, Enum):
    EQUALS = "EQUALS"
    LIKE = "LIKE"

"""DTO для REST API фильтрации"""
class FilterDTORest(BaseModel):
    field_name: str
    value: str
    filter_type: FilterTypeEnum
