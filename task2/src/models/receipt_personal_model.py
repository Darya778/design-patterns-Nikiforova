"""
Назначение: описание личного рецепта пользователя
"""

from src.models.receipt_model import receipt_model

class receipt_personal_model(receipt_model):
    """
    Модель пользовательского рецепта
    """

    def __init__(self, name: str, ingredients: list, unit: str, group: str, author: str):
        """
        :param author: автор рецепта
        """
        super().__init__(name, ingredients, unit, group)
        self.author = author

    def __repr__(self):
        return f"<PersonalReceipt {self.name} by {self.author}>"
