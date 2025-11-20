import unittest
from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.filter_dto import FilterDTO
from src.core.filters_enum import FilterType
from src.core.filter_utils import FilterUtils
from src.logics.osv_service import OSVPrototype


class MockStorage:
    """Mock хранилище для тестирования"""

    def __init__(self):
        gram = unit_model("грамм", 1)
        kilogram = unit_model("килограмм", 1000, base=gram)
        self.units = [gram, kilogram]

        group1 = group_model("Бакалея")
        group2 = group_model("Молочные продукты")
        self.groups = [group1, group2]

        nomenclature1 = nomenclature_model("Мука", full_name="Мука пшеничная", group=group1, unit=gram)
        nomenclature2 = nomenclature_model("Молоко", full_name="Молоко пастеризованное", group=group2, unit=kilogram)
        nomenclature3 = nomenclature_model("Сахар", full_name="Сахар белый", group=group1, unit=gram)
        self.nomenclatures = [nomenclature1, nomenclature2, nomenclature3]

        for index, nomenclature in enumerate(self.nomenclatures):
            nomenclature.balance = 1000 * (index + 1)

        self.convert_factory = type("convert_factory", (),
                                    {"convert": lambda self, obj: {"name": getattr(obj, "name", "")}})()


class TestFilterObjects(unittest.TestCase):
    """Тесты фильтрации объектов"""

    def setUp(self):
        self.storage = MockStorage()
        self.osv_proto = OSVPrototype(self.storage)

    def test_equals_filter(self):
        """Тест фильтрации по точному совпадению"""
        filters = [FilterDTO(field_name="name", value="Мука", filter_type=FilterType.EQUALS)]
        result = FilterUtils.apply(self.storage.nomenclatures, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Мука")

    def test_like_filter(self):
        """Тест фильтрации по подстроке"""
        filters = [FilterDTO(field_name="name", value="Мо", filter_type=FilterType.LIKE)]
        result = FilterUtils.apply(self.storage.nomenclatures, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Молоко")

    def test_nested_filter(self):
        """Тест фильтрации по вложенным полям"""
        filters = [FilterDTO(field_name="unit.name", value="грамм", filter_type=FilterType.EQUALS)]
        result = FilterUtils.apply(self.storage.nomenclatures, filters)
        self.assertEqual(len(result), 2)
        names = [n.name for n in result]
        self.assertIn("Мука", names)
        self.assertIn("Сахар", names)


class TestOSVPrototype(unittest.TestCase):
    """Тесты прототипа ОСВ"""

    def setUp(self):
        self.storage = MockStorage()
        self.osv_proto = OSVPrototype(self.storage)

    def test_generate_osv_no_filter(self):
        """Тест генерации ОСВ без фильтров"""
        osv = self.osv_proto.generate_osv("nomenclature")
        self.assertEqual(len(osv), 3)
        self.assertEqual(osv[0]["name"], "Мука")

    def test_generate_osv_with_filter(self):
        """Тест генерации ОСВ с фильтрами"""
        filters = [FilterDTO(field_name="group.name", value="Бакалея", filter_type=FilterType.EQUALS)]
        osv = self.osv_proto.generate_osv("nomenclature", filters)
        self.assertEqual(len(osv), 2)
        names = [o["name"] for o in osv]
        self.assertIn("Мука", names)
        self.assertIn("Сахар", names)


if __name__ == "__main__":
    unittest.main()
