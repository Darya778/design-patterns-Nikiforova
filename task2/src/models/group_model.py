"""
Модель группы номенклатуры (справочная), наследуется от abstract_reference
"""

from src.core.abstract_reference import abstract_reference

""" Группа номенклатуры. На данный момент содержит только наименование """
class group_model(abstract_reference):
    def __init__(self, name: str = ""):
        super().__init__(name)

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "name": self.name
        }
