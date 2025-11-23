"""
Domain-модель для snapshot'а оборотов до даты блокировки
"""
from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional, Dict, Any


@dataclass
class turnover_snapshot_model:
    """
    Модель для агрегированного снэпшота оборотов.
    Поля:
      - warehouse_id: Optional[int]  — id склада или None для 'всех'
      - item_id: int                 — id номенклатуры
      - unit_id: Optional[int]       — id единицы измерения
      - closing: float               — итоговый (закрывающий) остаток в базовой единице
      - snapshot_date: date          — дата расчёта (дата блокировки)
    """
    warehouse_id: Optional[int]
    item_id: int
    unit_id: Optional[int]
    closing: float
    snapshot_date: date

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует модель в словарь, готовый для записи в JSON.
        Преобразует дату в ISO-строку.
        """
        return {
            "warehouse_id": self.warehouse_id,
            "item_id": self.item_id,
            "unit_id": self.unit_id,
            "closing": self.closing,
            "snapshot_date": self.snapshot_date.isoformat() if self.snapshot_date else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], fallback_date: date = None) -> "turnover_snapshot_model":
        """
        Создаёт модель из словаря (как из JSON).
        Ожидается, что snapshot_date — строка ISO или None.
        """
        sd = data.get("snapshot_date", None)
        snap_date = date.fromisoformat(sd) if sd else fallback_date
        return cls(
            warehouse_id=data.get("warehouse_id"),
            item_id=data.get("item_id"),
            unit_id=data.get("unit_id"),
            closing=data.get("closing", 0.0),
            snapshot_date=snap_date
        )
