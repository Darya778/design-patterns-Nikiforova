"""
Domain-модель строки ОСВ (Оборотно-сальдовой ведомости)
"""
from dataclasses import dataclass
from typing import Optional
from src.models.warehouse_model import warehouse_model
from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model


@dataclass
class osv_row_model:
    """
    Строка ОСВ как доменная модель.
    """
    warehouse: Optional[warehouse_model]
    item: nomenclature_model
    unit: Optional[unit_model]
    opening: float
    incoming: float
    outgoing: float

    @property
    def closing(self) -> float:
        """
        Конечный остаток = начальный + приход - расход
        """
        return self.opening + self.incoming - self.outgoing
