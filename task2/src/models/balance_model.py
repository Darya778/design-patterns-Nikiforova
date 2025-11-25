class balance_model:
    def __init__(self, warehouse, item, unit, balance):
        self.warehouse = warehouse
        self.item = item
        self.unit = unit
        self.balance = balance

    def clone(self):
        return balance_model(
            warehouse=self.warehouse,
            item=self.item,
            unit=self.unit,
            balance=self.balance
        )

    def to_dict(self):
        return {
            "warehouse": self.warehouse.to_dict() if self.warehouse and hasattr(self.warehouse, "to_dict") else None,
            "item": self.item.to_dict() if self.item and hasattr(self.item, "to_dict") else None,
            "unit": self.unit.to_dict() if self.unit and hasattr(self.unit, "to_dict") else None,
            "balance": self.balance
        }
