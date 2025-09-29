import unittest
from src.models.company_model import company_model

"""
Юнит-тесты для модели company_model
"""
class TestCompanyModel(unittest.TestCase):

    def test_success_set_inn_with_12_digits(self):
        """
        Проверка установки корректного ИНН
        Входные данные: строка "123456789012" (12 цифр)
        Ожидание: значение устанавливается без ошибок
        """
        c = company_model(name="Test")
        c.inn = "123456789012"
        self.assertEqual(c.inn, "123456789012")

    def test_error_set_inn_with_invalid_length(self):
        """
        Проверка ошибки при установке некорректного ИНН
        Входные данные: строка "123" (3 цифры)
        Ожидание: возбуждается ValueError
        """
        c = company_model(name="Test")
        with self.assertRaises(ValueError):
            c.inn = "123"

    def test_success_set_account_and_corr_account_with_11_digits(self):
        """
        Проверка установки расчетного и корреспондентского счетов
        Входные данные: строки "12345678901" и "98765432109" (11 цифр)
        Ожидание: значения устанавливаются без ошибок
        """
        c = company_model(name="Test")
        c.account = "12345678901"
        c.corr_account = "98765432109"
        self.assertEqual(c.account, "12345678901")
        self.assertEqual(c.corr_account, "98765432109")

    def test_error_set_account_and_corr_account_with_invalid_length(self):
        """
        Проверка ошибки при установке неверных счетов
        Входные данные: "123" и "12"
        Ожидание: возбуждается ValueError
        """
        c = company_model(name="Test")
        with self.assertRaises(ValueError):
            c.account = "123"
        with self.assertRaises(ValueError):
            c.corr_account = "12"

    def test_success_set_bik_and_ownership_with_valid_values(self):
        """
        Проверка установки БИК и формы собственности
        Входные данные: "123456789" и "ООО"
        Ожидание: значения устанавливаются корректно
        При неверных значениях возбуждается ValueError
        """
        c = company_model(name="Test")
        c.bik = "123456789"
        self.assertEqual(c.bik, "123456789")
        with self.assertRaises(ValueError):
            c.bik = "123"
        c.ownership = "ООО"
        self.assertEqual(c.ownership, "ООО")
        with self.assertRaises(ValueError):
            c.ownership = "СЛИШКОМДЛИННО"

    def test_ignore_set_name_when_empty_string(self):
        """
        Проверка игнорирования пустой строки для имени
        Входные данные: строка "   "
        Ожидание: имя компании не меняется
        """
        c = company_model(name="Test")
        c.name = "   "
        self.assertEqual(c.name, "Test")

    def test_success_equality_and_repr_when_comparing_objects(self):
        """
        Проверка сравнения объектов и строкового представления
        Ожидание: объекты с одинаковыми данными равны,
        объекты с разными данными - не равны,
        repr содержит 'company_model'
        """
        c1 = company_model(name="Test", inn="123456789012")
        c2 = company_model(name="Test", inn="123456789012")
        c3 = company_model(name="Other", inn="000000000000")
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertIn("company_model", repr(c1))
