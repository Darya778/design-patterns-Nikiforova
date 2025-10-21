"""
Назначение: описание личного рецепта пользователя
"""

from src.models.receipt_model import receipt_model
from src.core.validator import validator, argument_exception

class receipt_personal_model(receipt_model):
    """
    Модель личного (пользовательского) рецепта
    """

    def __init__(
        self,
        name: str,
        ingredients: list,
        unit: str,
        group: str,
        author: str = "Неизвестен",
        portions: int = 1,
        steps: list[str] | None = None
    ):
        """
        :param author: автор рецепта
        :param portions: количество порций
        :param steps: список шагов приготовления
        """
        validator.validate(author, str)
        validator.validate(portions, int)
        validator.validate(steps if steps is not None else [], list)

        super().__init__(name, ingredients, unit, group)

        self.author = author
        self.portions = portions
        self.steps = steps if steps is not None else []

    def __repr__(self):
        return f"<PersonalReceipt {self.name} by {self.author}, steps={len(self.steps)}>"

    """ Возвращает словарь рецепта с учётом всех дополнительных полей """
    def to_dict(self):

        base = super().to_dict()
        base["author"] = self.author
        base["portions"] = self.portions
        base["steps"] = self.steps
        return base
