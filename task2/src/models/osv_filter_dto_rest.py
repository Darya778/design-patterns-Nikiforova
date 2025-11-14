from pydantic import BaseModel
from typing import List
from src.models.filter_dto_rest import FilterDTORest

"""Запрос для фильтрации оборотно-сальдовой ведомости"""
class OSVFilterRequest(BaseModel):
    model_type: str
    filters: List[FilterDTORest]
