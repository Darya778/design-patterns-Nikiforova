from src.models.company_model import company_model
from src.models.settings_manager import settings_manager
from src.models.settings import Settings
import os
import unittest
import json
import tempfile

class TestModels(unittest.TestCase):

    def test_empty_createmodel_company_model(self):
        model = company_model()
        assert model.name == ""

    def test_notEmpty_createmodel_company_model(self):
        model = company_model()
        model.name = "test"
        assert model.name != ""

    def test_load_createmodel_company_model(self):
        file_name = "D:/MY/pycharm/Patterns2025/settings.json"
        manager = settings_manager(file_name)
        result = manager.load()
        assert result == True

    def test_load_two_createmodel_company_model(self):
        file_name = "D:/MY/pycharm/Patterns2025/settings.json"
        manager1 = settings_manager(file_name)
        manager2 = settings_manager(file_name)
        manager1.load()
        # manager2.load()
        assert manager1.company == manager2.company


class TestCompanyModel(unittest.TestCase):

    def test_inn_valid_and_invalid(self):
        c = company_model()
        c.inn = "123456789012"
        self.assertEqual(c.inn, "123456789012")
        with self.assertRaises(ValueError):
            c.inn = "123"

    def test_name_setter_empty(self):
        c = company_model()
        c.name = "Test"
        self.assertEqual(c.name, "Test")
        c.name = "   "
        self.assertEqual(c.name, "Test")


class TestSettings(unittest.TestCase):

    def test_settings_validation(self):
        s = Settings(
            name="Компания",
            inn="123456789012",
            account="12345678901",
            corr_account="98765432109",
            bik="123456789",
            ownership="ЗАО  "
        )

        self.assertEqual(s.name, "Компания")
        self.assertEqual(s.inn, "123456789012")
        self.assertEqual(s.account, "12345678901")
        self.assertEqual(s.corr_account, "98765432109")
        self.assertEqual(s.bik, "123456789")
        self.assertEqual(s.ownership, "ЗАО  ")

    def test_settings_invalid_inn(self):
        with self.assertRaises(ValueError):
            Settings("Компания", "12345", "12345678901", "98765432109", "123456789", "ЗАО  ")

    def test_invalid_fields(self):
        with self.assertRaises(ValueError):
            Settings("Company", "12345", "12345678901", "98765432109", "123456789", "OOOOO")
        with self.assertRaises(ValueError):
            Settings("Company", "123456789012", "12345", "98765432109", "123456789", "OOOOO")
        with self.assertRaises(ValueError):
            Settings("Company", "123456789012", "12345678901", "12345", "123456789", "OOOOO")
        with self.assertRaises(ValueError):
            Settings("Company", "123456789012", "12345678901", "98765432109", "12345", "OOOOO")
        with self.assertRaises(ValueError):
            Settings("Company", "123456789012", "12345678901", "98765432109", "123456789", "AB")

    def test_name_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            Settings("", "123456789012", "12345678901", "98765432109", "123456789", "OOOOO")

class TestSettingsManager(unittest.TestCase):

    def test_load_from_other_dir(self):
        tmp_dir = tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, "custom_config.json")

        data = {
            "company": {
                "name": "TestCo",
                "inn": "123456789012",
                "account": "12345678901",
                "corr_account": "98765432109",
                "bik": "123456789",
                "ownership": "ЗАО  "
            }
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        loader = settings_manager(file_path)
        self.assertTrue(loader.load())
        self.assertEqual(loader.settings.inn, "123456789012")
        self.assertEqual(loader.settings.account, "12345678901")
        self.assertEqual(loader.company.name, "TestCo")

    def test_load_without_filename(self):
        sm = settings_manager("   ")
        sm._settings_manager__file_name = ""
        with self.assertRaises(Exception):
            sm.load()

    def test_load_invalid_json(self):
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")

        sm = settings_manager(tmp_path)
        self.assertFalse(sm.load())

        os.remove(tmp_path)

    def test_convert_and_default(self):
        sm = settings_manager("   ")
        sm.default()
        self.assertEqual(sm.company.name, "Рога и копыта")

        data = {
            "name": "TestCo",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "98765432109",
            "bik": "123456789",
            "ownership": "OOOOO"
        }
        settings_obj = sm.convert(data)
        self.assertIsInstance(settings_obj, Settings)
        self.assertEqual(settings_obj.inn, "123456789012")


if __name__ == "__main__":
    unittest.main()

