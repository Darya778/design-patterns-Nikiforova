import unittest
from src.models.settings_model import SettingsModel, ResponseFormat
from src.core.factory_entities import FactoryEntities

""" Набор модульных тестов для проверки корректности работы фабрики форматов """
class TestFactoryEntities(unittest.TestCase):

    """ Подготовка тестовых данных """
    def setUp(self):
        self.data = [
            {"id": 1, "name": "Item1"},
            {"id": 2, "name": "Item2"}
        ]

    """ Проверка генерации Markdown-таблицы """
    def test_markdown_format(self):
        settings = SettingsModel(response_format=ResponseFormat.Markdown)
        factory = FactoryEntities(settings)
        result = factory.create_default(self.data)
        self.assertIn("| id | name |", result)

    """ Проверка генерации JSON-структуры """
    def test_json_format(self):
        settings = SettingsModel(response_format=ResponseFormat.JSON)
        factory = FactoryEntities(settings)
        result = factory.create_default(self.data)
        self.assertTrue(result.strip().startswith("["))

    """Проверка генерации XML-документа."""
    def test_xml_format(self):
        settings = SettingsModel(response_format=ResponseFormat.XML)
        factory = FactoryEntities(settings)
        result = factory.create_default(self.data)
        self.assertIn("<Item>", result)

    """ Проверка генерации CSV-таблицы """
    def test_csv_format(self):
        settings = SettingsModel(response_format=ResponseFormat.CSV)
        factory = FactoryEntities(settings)
        result = factory.create_default(self.data)
        self.assertIn("id,name", result)
