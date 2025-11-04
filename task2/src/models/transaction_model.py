"""
Модель транзакции (учёт движения номенклатуры по складам)
"""

from datetime import date
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model
from src.models.unit_model import unit_model
from src.core.validator import validator, argument_exception


class transaction_model:
    """
    Транзакция движения номенклатуры по складам
    """

    def __init__(self, number: str, nomenclature: nomenclature_model,
                 warehouse: warehouse_model, quantity: float,
                 unit: unit_model, date_: date):
        validator.validate(number, str)
        validator.validate(quantity, (int, float))

        if not isinstance(nomenclature, nomenclature_model):
            raise argument_exception("nomenclature должен быть экземпляром nomenclature_model")
        if not isinstance(warehouse, warehouse_model):
            raise argument_exception("warehouse должен быть экземпляром warehouse_model")
        if not isinstance(unit, unit_model):
            raise argument_exception("unit должен быть экземпляром unit_model")

        self.number = number
        self.nomenclature = nomenclature
        self.warehouse = warehouse
        self.quantity = float(quantity)
        self.unit = unit
        self.date = date_

    @property
    def code(self):
        """Возвращает уникальный код (равен number)"""
        return self.number

    def to_dict(self):
        """Полная сериализация для сохранения"""
        return {
            "id": getattr(self, "id", None),
            "number": self.number,
            "date": self.date.isoformat(),
            "nomenclature": {
                "id": getattr(self.nomenclature, "id", None),
                "name": self.nomenclature.name
            },
            "warehouse": {
                "id": getattr(self.warehouse, "id", None),
                "name": self.warehouse.name,
                "code": getattr(self.warehouse, "code", None)
            },
            "quantity": self.quantity,
            "unit": {
                "id": getattr(self.unit, "id", None),
                "name": self.unit.name,
                "factor": self.unit.factor
            }
        }

