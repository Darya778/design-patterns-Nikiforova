"""
Назначение: хранилище данных для моделей проекта
"""

class storage_repository:
    """
    Репозиторий для хранения всех моделей приложения
    """

    def __init__(self):
        self.nomenclatures = []
        self.units = []
        self.groups = []
        self.receipts = []

    def add_nomenclature(self, item):
        self.nomenclatures.append(item)

    def add_unit(self, item):
        self.units.append(item)

    def add_group(self, item):
        self.groups.append(item)

    def add_receipt(self, item):
        self.receipts.append(item)
