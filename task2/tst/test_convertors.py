import unittest
from datetime import datetime
from src.core.convertors import (
    basic_convertor,
    datetime_convertor,
    reference_convertor
)
from src.logics.convert_factory import convert_factory


class DummyReference:
    """Вспомогательный класс для имитации ссылочного объекта."""
    def __init__(self, code, name):
        self.code = code
        self.name = name


class TestConvertors(unittest.TestCase):
    """Проверяет корректность работы отдельных конверторов."""

    def test_returns_value_convert_basic_types(self):
        """
        Проверяет, что basic_convertor возвращает само значение (int или str),
        а не словарь.
        """
        conv = basic_convertor()
        self.assertEqual(conv.convert(10), 10)
        self.assertEqual(conv.convert("abc"), "abc")

    def test_returns_string_convert_datetime(self):
        """
        Проверяет, что datetime_convertor возвращает строку в ISO-формате.
        """
        conv = datetime_convertor()
        dt = datetime(2025, 10, 24, 10, 30)
        result = conv.convert(dt)
        self.assertIsInstance(result, str)
        self.assertIn("2025-10-24", result)

    def test_returns_code_and_name_convert_reference_object(self):
        """
        Проверяет, что reference_convertor корректно возвращает словарь
        с ключами 'code' и 'name' для ссылочного объекта.
        """
        conv = reference_convertor()
        ref = DummyReference("R001", "TestRef")
        self.assertEqual(conv.convert(ref), {"code": "R001", "name": "TestRef"})


class TestConvertFactory(unittest.TestCase):
    """Проверяет работу фабрики convert_factory."""

    def setUp(self):
        self.factory = convert_factory()

    def test_returns_value_convert_basic_types(self):
        """
        Проверяет, что convert_factory возвращает исходные значения
        для простых типов данных (int, str).
        """
        self.assertEqual(self.factory.convert(5), 5)
        self.assertEqual(self.factory.convert("x"), "x")

    def test_returns_string_convert_datetime(self):
        """
        Проверяет, что convert_factory возвращает строку
        для объектов datetime в ISO-формате.
        """
        dt = datetime(2025, 10, 24, 11, 0)
        result = self.factory.convert(dt)
        self.assertIsInstance(result, str)
        self.assertIn("2025-10-24", result)

    def test_returns_dictionary_convert_reference_object(self):
        """
        Проверяет, что convert_factory корректно обрабатывает
        ссылочные объекты (code, name).
        """
        ref = DummyReference("C02", "RefName")
        self.assertEqual(
            self.factory.convert(ref),
            {"code": "C02", "name": "RefName"}
        )

    def test_returns_list_convert_collection_mixed_types(self):
        """
        Проверяет, что convert_factory корректно обрабатывает коллекции
        из разных типов и возвращает список конвертированных элементов.
        """
        items = [1, "a", datetime(2025, 1, 1)]
        results = self.factory.convert_collection(items)
        self.assertEqual(len(results), 3)
