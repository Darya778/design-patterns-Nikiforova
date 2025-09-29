"""
Модель склада (простая справочная модель)
"""

from src.core.abstract_reference import abstract_reference

""" Справочная модель склада """
class warehouse_model(abstract_reference):
    def __init__(self, name: str = ""):
        super().__init__(name)
