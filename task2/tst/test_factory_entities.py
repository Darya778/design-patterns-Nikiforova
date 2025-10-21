import unittest
from src.models.settings_model import settings_model, ResponseFormat
from src.logics.factory_entities import factory_entities

""" Набор модульных тестов для проверки корректности работы фабрики форматов """
class test_factory_entities(unittest.TestCase):

    """ Подготовка тестовых данных """
    def setUp(self):
        self.data = [{"name": "Тест", "unit": "грамм"}]

    """ Проверка генерации Markdown-таблицы """
    def test_create_default_returns_markdown(self):
        settings = settings_model(response_format=ResponseFormat.Markdown)
        factory = factory_entities(settings)
        result = factory.create_default(self.data)
        self.assertIn("# Тест", result)
        self.assertIn("**Порций:**", result)

    """ Проверка генерации JSON-структуры """
    def test_create_default_returns_json(self):
        settings = settings_model(response_format=ResponseFormat.JSON)
        factory = factory_entities(settings)
        result = factory.create_default(self.data)
        self.assertTrue(result.strip().startswith("["))

    """Проверка генерации XML-документа."""
    def test_create_default_returns_xml(self):
        settings = settings_model(response_format=ResponseFormat.XML)
        factory = factory_entities(settings)
        result = factory.create_default(self.data)
        self.assertIn("<Item>", result)

    """ Проверка генерации CSV-таблицы """
    def test_create_default_returns_csv(self):
        settings = settings_model(response_format=ResponseFormat.CSV)
        factory = factory_entities(settings)
        result = factory.create_default(self.data)
        self.assertIn("name", result)
