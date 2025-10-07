"""
Назначение: создание и инициализация данных приложения
"""

from src.core.storage_repository import storage_repository
from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.receipt_model import receipt_model
from src.models.receipt_personal_model import receipt_personal_model


class start_service:
    """
    Класс для инициализации базовых данных проекта
    """

    def __init__(self, storage: storage_repository):
        """
        :param storage: экземпляр репозитория данных
        """
        self.storage = storage

    def create(self):
        """
        Создает тестовые данные:
        - Номенклатуру
        - Единицы измерения
        - Группы
        - Рецепты
        """
        self.__create_nomenclatures()
        self.__create_units()
        self.__create_groups()
        self.create_receipts()

    def __create_nomenclatures(self):
        """Создает базовую номенклатуру"""
        noms = [
            nomenclature_model("Мука"),
            nomenclature_model("Молоко"),
            nomenclature_model("Сахар"),
            nomenclature_model("Яйца"),
            nomenclature_model("Масло сливочное")
        ]
        for n in noms:
            self.storage.add_nomenclature(n)

    def __create_units(self):
        """Создает единицы измерения"""
        gram = unit_model("грамм", 1) 
        kilogram = unit_model("килограмм", 1000, base=gram)
        liter = unit_model("литр", 1)
        milliliter = unit_model("миллилитр", 1000, base=liter)
        piece = unit_model("штука", 1)

        for u in (gram, kilogram, liter, milliliter, piece):
            self.storage.add_unit(u)

    def __create_groups(self):
        """Создает группы продуктов"""
        groups = [
            group_model("Молочные продукты"),
            group_model("Бакалея"),
            group_model("Выпечка")
        ]
        for g in groups:
            self.storage.add_group(g)

    def create_receipts(self):
        """Создает тестовые рецепты"""
        base = receipt_model(
            name="Блины классические",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[1], self.storage.nomenclatures[3]],
            unit="грамм",
            group="Выпечка"
        )

        personal = receipt_personal_model(
            name="Панкейки по-домашнему",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[2], self.storage.nomenclatures[3]],
            unit="грамм",
            group="Выпечка",
            author="Дарья"
        )

        lesson = receipt_model(
            name="Блины с начинкой",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[1], self.storage.nomenclatures[4]],
            unit="грамм",
            group="Выпечка"
        )

        for r in (base, personal, lesson):
            self.storage.add_receipt(r)
