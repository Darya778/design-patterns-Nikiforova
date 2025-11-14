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
from src.core.id_generator import gen_id
import os


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

        if os.path.exists("task2/data_out/repository.json"):
            self.storage.load_all()
            return

        if not first_start:
            return

        if not self.storage.units:
            self.__create_units()
        if not self.storage.groups:
            self.__create_groups()
        if not self.storage.warehouses:
            self.__create_warehouses()
        if not self.storage.nomenclatures:
            self.__create_nomenclatures()
        if not self.storage.receipts:
            self.__create_receipts()
        if not self.storage.transactions:
            self.__create_transactions()

        self.storage.save_all()
        print("[OK] Репозиторий сохранён в файл.")

    def __create_nomenclatures(self):
        """Создаёт номенклатуры с полными ссылками на группы и единицы измерения"""
        groups = {g.name: g for g in self.storage.groups}
        units = {u.name: u for u in self.storage.units}

        noms = [
            nomenclature_model("Мука", full_name="Мука пшеничная", group=groups["Бакалея"], unit=units["грамм"]),
            nomenclature_model("Молоко", full_name="Молоко пастеризованное 3.2%", group=groups["Молочные продукты"], unit=units["литр"]),
            nomenclature_model("Сахар", full_name="Сахар белый", group=groups["Бакалея"], unit=units["грамм"]),
            nomenclature_model("Яйца", full_name="Яйца куриные", group=groups["Выпечка"], unit=units["штука"]),
            nomenclature_model("Масло сливочное", full_name="Масло сливочное 82.5%", group=groups["Молочные продукты"], unit=units["грамм"])
        ]

        for n in noms:
            n.id = gen_id("N")
            self.storage.add_nomenclature(n)

    def __create_units(self):
        gram = unit_model("грамм", 1)
        gram.id = gen_id("U")

        kilogram = unit_model("килограмм", 1000, base=gram)
        kilogram.id = gen_id("U")

        liter = unit_model("литр", 1)
        liter.id = gen_id("U")

        milliliter = unit_model("миллилитр", 1000, base=liter)
        milliliter.id = gen_id("U")

        piece = unit_model("штука", 1)
        piece.id = gen_id("U")

        for u in (gram, kilogram, liter, milliliter, piece):
            self.storage.add_unit(u)

    def __create_groups(self):
        g1 = group_model("Молочные продукты"); g1.id = gen_id("G")
        g2 = group_model("Бакалея"); g2.id = gen_id("G")
        g3 = group_model("Выпечка"); g3.id = gen_id("G")

        for g in (g1, g2, g3):
            self.storage.add_group(g)

    def __create_warehouses(self):
        """Создает справочник складов"""
        w1 = warehouse_model("Основной склад"); w1.id = gen_id("W"); w1.code = "MAIN"
        w2 = warehouse_model("Резервный склад"); w2.id = gen_id("W"); w2.code = "RES"

        for w in (w1, w2):
            self.storage.add_warehouse(w)

    def __create_receipts(self):
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
        base.id = gen_id("RC")

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
        personal.id = gen_id("RC")

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
        lesson.id = gen_id("RC")

        for r in (base, personal, lesson):
            self.storage.add_receipt(r)

    def __create_transactions(self):
        """Создает примерные транзакции"""
        nom = {n.name: n for n in self.storage.nomenclatures}
        wh = {w.name: w for w in self.storage.warehouses}
        units = {u.name: u for u in self.storage.units}

        txs = [
            transaction_model("T001", nom["Мука"], wh["Основной склад"], 5000, units["грамм"], date(2025, 1, 1)),
            transaction_model("T002", nom["Мука"], wh["Основной склад"], -1500, units["грамм"], date(2025, 1, 10)),
            transaction_model("T003", nom["Молоко"], wh["Основной склад"], 8, units["литр"], date(2025, 1, 5)),
            transaction_model("T004", nom["Сахар"], wh["Резервный склад"], 2000, units["грамм"], date(2025, 1, 3))
        ]
        for t in txs:
            t.id = gen_id("TX")
            self.storage.add_transaction(t)
