import unittest
from src.models.company_model import company_model
from src.models.settings_model import settings_model

class test_settings_model(unittest.TestCase):

    def test_success_assign_company_with_valid_object(self):
        """
        Проверка установки company в settings_model
        Входные данные: корректный company_model
        Ожидание: объект сохраняется, свойства доступны
        """
        company = company_model(name="Компания", inn="123456789012", account="12345678901",
                                corr_account="98765432109", bik="123456789", ownership="ЗАО")
        s = settings_model(company=company)
        self.assertEqual(s.company.name, "Компания")

    def test_error_assign_company_with_invalid_type(self):
        """
        Проверка ошибки при установке некорректного значения company
        Входные данные: строка "not_a_company_model"
        Ожидание: возбуждается Exception
        """
        with self.assertRaises(Exception):
            settings_model(company="not_a_company_model")

    def test_success_repr_contains_class_name(self):
        """
        Проверка строкового представления settings_model
        Ожидание: repr содержит "settings_model"
        """
        company = company_model(name="Компания", inn="123456789012")
        s = settings_model(company=company)
        self.assertIn("settings_model", repr(s))
