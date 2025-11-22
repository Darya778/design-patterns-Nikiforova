"""
Domain-модель для snapshot'а оборотов до даты блокировки
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class turnover_snapshot_model:
    """
    Модель, описывающая агрегированный снэпшот оборотов для
    конкретной комбинации (склад, номенклатура, единица).
    """
    warehouse_id: Optional[int]
    item_id: int
    unit_id: Optional[int]
    closing: float
    snapshot_date: date
