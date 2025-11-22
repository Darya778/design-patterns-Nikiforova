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
