"""
Назначение: создание и инициализация данных приложения
"""

from datetime import date
from src.core.storage_repository import storage_repository
from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.receipt_model import receipt_model
from src.models.receipt_personal_model import receipt_personal_model
from src.models.warehouse_model import warehouse_model
from src.models.transaction_model import transaction_model
from src.settings_manager import settings_manager


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
        - Склады
        - Транзакции
        При условии, что в настройках first_start == True (по умолчанию True).
        """
        try:
            settings = settings_manager()
            settings.default()
            first_start = getattr(settings, "first_start", True)
        except Exception:
            first_start = True

        if not first_start:
            return

        if not self.storage.nomenclatures:
            self.__create_nomenclatures()
        if not self.storage.units:
            self.__create_units()
        if not self.storage.groups:
            self.__create_groups()
        if not self.storage.receipts:
            self.create_receipts()
        if not self.storage.warehouses:
            self.__create_warehouses()
        if not self.storage.transactions:
            self.__create_transactions()

    def __create_nomenclatures(self):
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
        gram = unit_model("грамм", 1)
        kilogram = unit_model("килограмм", 1000, base=gram)
        liter = unit_model("литр", 1)
        milliliter = unit_model("миллилитр", 1000, base=liter)
        piece = unit_model("штука", 1)
        for u in (gram, kilogram, liter, milliliter, piece):
            self.storage.add_unit(u)

    def __create_groups(self):
        groups = [
            group_model("Молочные продукты"),
            group_model("Бакалея"),
            group_model("Выпечка")
        ]
        for g in groups:
            self.storage.add_group(g)

    def create_receipts(self):
        base = receipt_model(
            name="Блины классические",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[1], self.storage.nomenclatures[3]],
            unit="грамм",
            group="Выпечка",
            author="Классический рецепт",
            portions=4,
            steps=[
                "Смешайте муку, яйца и молоко до однородной массы.",
                "Добавьте немного соли и сахара по вкусу.",
                "Обжаривайте блины с двух сторон до золотистого цвета."
            ],
            code="R001"
        )

        personal = receipt_personal_model(
            name="Панкейки по-домашнему",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[2], self.storage.nomenclatures[3]],
            unit="грамм",
            group="Выпечка",
            author="Дарья",
            portions=6,
            steps=[
                "Взбейте яйца с сахаром.",
                "Добавьте муку и перемешайте до густоты.",
                "Выпекайте на сухой сковороде."
            ],
            code="R002"
        )

        lesson = receipt_model(
            name="Блины с начинкой",
            ingredients=[self.storage.nomenclatures[0], self.storage.nomenclatures[1], self.storage.nomenclatures[4]],
            unit="грамм",
            group="Выпечка",
            author="Учебный пример",
            portions=5,
            steps=[
                "Приготовьте тесто для блинов.",
                "Обжарьте блины и смажьте сливочным маслом.",
                "Добавьте начинку и сверните."
            ],
            code="R003"
        )

        for r in (base, personal, lesson):
            self.storage.add_receipt(r)

    def __create_warehouses(self):
        """Создает справочник складов"""
        for name in ("Основной склад", "Резервный склад"):
            self.storage.add_warehouse(warehouse_model(name))

    def __create_transactions(self):
        """Создает примерные транзакции"""
        txs = [
            transaction_model("T001", "Мука", "Основной склад", 5000, "грамм", date(2025, 1, 1)),
            transaction_model("T002", "Мука", "Основной склад", -1500, "грамм", date(2025, 1, 10)),
            transaction_model("T003", "Молоко", "Основной склад", 8, "литр", date(2025, 1, 5)),
            transaction_model("T004", "Сахар", "Резервный склад", 2000, "грамм", date(2025, 1, 3))
        ]
        for t in txs:
            self.storage.add_transaction(t)
