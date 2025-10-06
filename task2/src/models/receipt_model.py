"""
Назначение: базовая модель описания рецепта
"""

class receipt_model:
    """
    Класс описывает базовый рецепт
    """

    def __init__(self, name: str, ingredients: list, unit: str, group: str):
        """
        :param name: наименование рецепта
        :param ingredients: список ингредиентов (объекты nomenclature_model)
        :param unit: единица измерения
        :param group: группа рецепта
        """
        self.name = name
        self.ingredients = ingredients
        self.unit = unit
        self.group = group

    def __repr__(self):
        return f"<Receipt {self.name}, {len(self.ingredients)} ingredients>"
