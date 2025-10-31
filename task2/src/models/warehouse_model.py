"""
Модель склада (простая справочная модель)
"""

from src.core.abstract_reference import abstract_reference

""" Справочная модель склада """
class warehouse_model(abstract_reference):
    def __init__(self, name: str = "", code: str = None):
        super().__init__(name)
        self.code = code or self._generate_code(name)

    def _generate_code(self, name: str):
        return name[:3].upper().replace(" ", "")

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code
        }
