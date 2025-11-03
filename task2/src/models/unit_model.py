"""
Модель единицы измерения с опцией базовой единицы и коэффициента пересчёта
"""

from typing import Optional
from src.core.abstract_reference import abstract_reference
from src.core.validator import validator, argument_exception

"""
Единица измерения
Атрибуты:
    factor: коэффициент пересчёта в отношении к базовой единице (int > 0)
    base: ссылка на базовую единицу (unit_model) или None (самая базовая)
"""
class unit_model(abstract_reference):
    __factor: int = 1
    __base: Optional["unit_model"] = None

    """
    Инициализация единицы измерения

    Args:
        name: наименование (до 50 символов)
        factor: коэффициент пересчёта (целое > 0)
        base: базовая единица (unit_model) или None
    """
    def __init__(self, name: str, factor: int = 1, base: "unit_model" = None):
        super().__init__(name)

        validator.validate(factor, int)
        if factor <= 0:
            raise argument_exception("factor должен быть положительным целым числом")
        self.__factor = factor

        if base is not None and not isinstance(base, unit_model):
            raise argument_exception("base должен быть экземпляром unit_model или None")
        self.__base = base

    """ Коэффициент пересчёта (в целых единицах относительно базовой) """
    @property
    def factor(self) -> int:
        return self.__factor

    """ Базовая единица (или None, если данная — базовая) """
    @property
    def base(self) -> Optional["unit_model"]:
        return self.__base

    """
    Перевести значение в базовую единицу
    Если base отсутствует, возвращает value * 1
    """
    def to_base(self, value: float) -> float:
        validator.validate(value, (int, float))
        return value * self.__factor

    """ Перевести значение из базовой единицы в текущую """
    def from_base(self, value: float) -> float:
        if self.__factor == 0:
            raise argument_exception("factor не может быть нулевым")
        validator.validate(value, (int, float))
        return value / self.__factor

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "name": self.name,
            "factor": self.factor,
            "base": self.__base.to_dict() if self.__base else None
        }
