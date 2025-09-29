import os
import json
import tempfile
import unittest
from src.settings_manager import settings_manager

class test_settings_manager(unittest.TestCase):

    def test_success_load_file_with_valid_json(self):
        """
        Проверка загрузки корректного JSON
        Ожидание: метод load возвращает True, компания инициализируется
        """
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        data = {"company": {
            "name": "TestCo",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "98765432109",
            "bik": "123456789",
            "ownership": "ООО"
        }}
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        sm = settings_manager(tmp_path)
        self.assertTrue(sm.load())
        self.assertEqual(sm.company.name, "TestCo")
        os.remove(tmp_path)

    def test_error_load_file_missing_company_key(self):
        """
        Проверка загрузки JSON без ключа company
        Ожидание: метод load возвращает False
        """
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump({"wrong_key": {}}, f, ensure_ascii=False)
        sm = settings_manager(tmp_path)
        self.assertFalse(sm.load())
        os.remove(tmp_path)

    def test_error_load_file_invalid_json(self):
        """
        Проверка загрузки некорректного JSON
        Ожидание: метод load возвращает False
        """
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")
        sm = settings_manager(tmp_path)
        self.assertFalse(sm.load())
        os.remove(tmp_path)

    def test_success_default_method(self):
        """
        Проверка метода default
        Ожидание: устанавливается компания "Рога и копыта"
        """
        sm = settings_manager("   ")
        sm.default()
        self.assertEqual(sm.company.name, "Рога и копыта")

    def test_success_singleton_behavior(self):
        """
        Проверка работы Singleton-паттерна
        Ожидание: два экземпляра settings_manager указывают на один объект
        """
        sm1 = settings_manager("settings.json")
        sm2 = settings_manager("settings.json")
        self.assertIs(sm1, sm2)

    def test_ignore_file_name_setter_invalid_path(self):
        """
        Проверка установки file_name
        Входные данные: несуществующий путь
        Ожидание: значение file_name не меняется
        """
        sm = settings_manager("settings.json")
        old_file = sm.file_name
        sm.file_name = "non_existing_path.json"
        self.assertEqual(sm.file_name, old_file)
