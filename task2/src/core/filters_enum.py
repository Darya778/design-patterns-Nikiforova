from enum import Enum

"""Типы фильтров для операций сравнения"""
class FilterType(Enum):
    EQUALS = "equals"
    LIKE = "like"
