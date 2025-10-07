"""
Назначение: базовая модель описания рецепта
"""

from src.core.validator import validator, argument_exception


class receipt_model:
    """
    Класс описывает базовый рецепт.
    Содержит данные о названии, ингредиентах, единице измерения и группе.
    """

    def __init__(self, name: str, ingredients: list, unit: str, group: str):
        """
        Инициализация модели рецепта

        :param name: наименование рецепта
        :param ingredients: список ингредиентов (объекты nomenclature_model)
        :param unit: единица измерения
        :param group: группа рецепта
        """

        try:
            validator.validate(name, str)
            validator.validate(unit, str)
            validator.validate(group, str)
            validator.validate(ingredients, list)
        except argument_exception:
            raise argument_exception("Неверные аргументы при создании рецепта")

        self.__name = name
        self.__ingredients = ingredients
        self.__unit = unit
        self.__group = group

    @property
    def name(self) -> str:
        """Наименование рецепта"""
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value

    @property
    def ingredients(self) -> list:
        """Список ингредиентов"""
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: list):
        validator.validate(value, list)
        self.__ingredients = value

    @property
    def unit(self) -> str:
        """Единица измерения"""
        return self.__unit

    @unit.setter
    def unit(self, value: str):
        validator.validate(value, str)
        self.__unit = value

    @property
    def group(self) -> str:
        """Группа рецепта"""
        return self.__group

    @group.setter
    def group(self, value: str):
        validator.validate(value, str)
        self.__group = value

    def __repr__(self):
        return f"<Receipt name={self.__name}, ingredients={len(self.__ingredients)}, unit={self.__unit}, group={self.__group}>"
