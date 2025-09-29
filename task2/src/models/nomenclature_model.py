"""
Модель номенклатуры. Содержит: name (ограничение 50), full_name (<=255),
ссылки на group_model и unit_model (unit_model)
"""

from src.core.abstract_reference import abstract_reference
from src.core.validator import validator, argument_exception
from src.models.group_model import group_model
from src.models.unit_model import unit_model

""" Номенклатурная позиция """
class nomenclature_model(abstract_reference):

    __full_name: str = ""
    __group: group_model = None
    __unit: unit_model = None

    def __init__(self, name: str = "", full_name: str = "", group: group_model = None,
                 unit: unit_model = None):
        super().__init__(name)
        if full_name:
            self.full_name = full_name
        if group is not None:
            self.group = group
        if unit is not None:
            self.unit = unit

    """ Полное наименование (<=255 символов) """
    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        validator.validate(value, str, max_length=255)
        self.__full_name = value.strip()

    """ Группа номенклатуры (group_model) """
    @property
    def group(self) -> group_model:
        return self.__group

    @group.setter
    def group(self, value: group_model):
        if not isinstance(value, group_model):
            raise argument_exception("group должен быть экземпляром group_model")
        self.__group = value

    """ Единица измерения (unit_model) """
    @property
    def unit(self) -> unit_model:
        return self.__unit

    @unit.setter
    def unit(self, value: unit_model):
        if not isinstance(value, unit_model):
            raise argument_exception("unit должен быть экземпляром unit_model")
        self.__unit = value
