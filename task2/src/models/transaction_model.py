"""
Модель транзакции (учёт движения номенклатуры по складам)
"""

from datetime import date

class transaction_model:
    """
    Модель Транзакции
    Отражает движение номенклатуры по складам
    """

    def __init__(
        self,
        number: str,
        nomenclature: str,
        warehouse: str,
        quantity: float,
        unit: str,
        date_: date
    ):
        self.number = number
        self.nomenclature = nomenclature
        self.warehouse = warehouse
        self.quantity = float(quantity)
        self.unit = unit
        self.date = date_

    def to_dict(self):
        return {
            "number": self.number,
            "nomenclature": self.nomenclature,
            "warehouse": self.warehouse,
            "quantity": self.quantity,
            "unit": self.unit,
            "date": self.date.isoformat()
        }
