"""
Назначение: базовая модель описания рецепта
"""

from src.core.validator import validator, argument_exception


class receipt_model:
    """
    Класс описывает базовый рецепт.
    Содержит данные о названии, ингредиентах, единице измерения и группе.
    """

    def __init__(self, name: str, ingredients: list, unit: str, group: str,
                 author: str = "Неизвестен", portions: int = 1, steps: list = None):
        """
        Инициализация модели рецепта

        :param name: наименование рецепта
        :param ingredients: список ингредиентов (объекты nomenclature_model)
        :param unit: единица измерения
        :param group: группа рецепта
        :param author: автор рецепта
        :param portions: количество порций
        :param steps: шаги приготовления
        """

        try:
            validator.validate(name, str)
            validator.validate(unit, str)
            validator.validate(group, str)
            validator.validate(ingredients, list)
            validator.validate(author, str)
            validator.validate(portions, int)
            if steps is not None:
                validator.validate(steps, list)
        except argument_exception:
            raise argument_exception("Неверные аргументы при создании рецепта")

        self.__name = name
        self.__ingredients = ingredients
        self.__unit = unit
        self.__group = group
        self.__author = author
        self.__portions = portions
        self.__steps = steps or []  # если None — создаем пустой список

    # --- Свойства ---

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

    @property
    def author(self) -> str:
        """Автор рецепта"""
        return self.__author

    @author.setter
    def author(self, value: str):
        validator.validate(value, str)
        self.__author = value

    @property
    def portions(self) -> int:
        """Количество порций"""
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        validator.validate(value, int)
        self.__portions = value

    @property
    def steps(self) -> list:
        """Пошаговое приготовление"""
        return self.__steps

    @steps.setter
    def steps(self, value: list):
        validator.validate(value, list)
        self.__steps = value


    def __repr__(self):
        return f"<Receipt name={self.__name}, ingredients={len(self.__ingredients)}, unit={self.__unit}, group={self.__group}>"

    """ Преобразование модели рецепта в словарь для форматтеров (CSV, JSON, XML, MD) """
    def to_dict(self):
        return {
            "name": self.name,
            "group": self.group,
            "unit": self.unit,
            "author": self.author,
            "portions": self.portions,
            "ingredients": [i.name if hasattr(i, "name") else str(i) for i in self.ingredients],
            "steps": [str(s) for s in self.steps] if self.steps else [],
        }
