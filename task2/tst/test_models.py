from src.models.company_model import company_model
from src.models.settings_manager import settings_manager
from src.models.settings import Settings
import os
import unittest
import json
import tempfile

class TestModels(unittest.TestCase):

    def test_empty_createmodel_company_model(self):
        model = company_model(name="")
        assert model.name == ""

    def test_notEmpty_createmodel_company_model(self):
        model = company_model(name="test")
        assert model.name != ""

    def test_load_createmodel_company_model(self):
        sm = settings_manager("settings.json")
        result = sm.load()
        assert result is True

    def test_load_two_createmodel_company_model(self):
        sm1 = settings_manager("settings.json")
        sm2 = settings_manager("settings.json")
        sm1.load()
        sm2.load()
        assert sm1.company == sm2.company


class TestCompanyModel(unittest.TestCase):

    def test_inn_valid_and_invalid(self):
        c = company_model(name="Test")
        c.inn = "123456789012"
        assert c.inn == "123456789012"
        with self.assertRaises(ValueError):
            c.inn = "123"

    def test_account_and_corr_account_validation(self):
        c = company_model(name="Test")
        c.account = "12345678901"
        assert c.account == "12345678901"
        with self.assertRaises(ValueError):
            c.account = "123"

        c.corr_account = "98765432109"
        assert c.corr_account == "98765432109"
        with self.assertRaises(ValueError):
            c.corr_account = "12"

    def test_bik_and_ownership_validation(self):
        c = company_model(name="Test")
        c.bik = "123456789"
        assert c.bik == "123456789"
        with self.assertRaises(ValueError):
            c.bik = "123"

        c.ownership = "ООО"
        assert c.ownership == "ООО"

        with self.assertRaises(ValueError):
            c.ownership = "СЛИШКОМДЛИННО"

    def test_name_setter_empty(self):
        c = company_model(name="Test")
        assert c.name == "Test"
        c.name = "   "
        assert c.name == "Test"

    def test_repr_and_eq(self):
        c1 = company_model(name="Test", inn="123456789012")
        c2 = company_model(name="Test", inn="123456789012")
        c3 = company_model(name="Other", inn="000000000000")
        assert repr(c1).startswith("company_model(")
        assert c1 == c2
        assert c1 != c3


class TestSettings(unittest.TestCase):

    def test_settings_validation(self):
        company = company_model(
            name="Компания",
            inn="123456789012",
            account="12345678901",
            corr_account="98765432109",
            bik="123456789",
            ownership="ЗАО"
        )

        s = Settings(company=company)
        assert s.company.name == "Компания"
        assert s.log_level == "INFO"
        assert "Settings(" in repr(s)

    def test_settings_invalid_company(self):
        with self.assertRaises(ValueError):
            Settings(company="not_a_company_model")


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
                "ownership": "ЗАО"
            }
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        loader = settings_manager(file_path)
        assert loader.load()
        assert loader.settings.company.name == "TestCo"
        assert loader.settings.company.inn == "123456789012"

        os.remove(file_path)

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
        assert not sm.load()

        os.remove(tmp_path)

    def test_convert_and_default(self):
        sm = settings_manager("   ")
        sm.default()
        assert sm.company.name == "Рога и копыта"

        data = {
            "name": "TestCo",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "98765432109",
            "bik": "123456789",
            "ownership": "ООО"
        }
        settings_obj = sm.convert(data)
        assert isinstance(settings_obj, Settings)
        assert settings_obj.company.inn == "123456789012"

    def test_load_with_relative_path(self):
        tmp_dir = os.path.join(os.path.dirname(__file__), "../src/data")
        os.makedirs(tmp_dir, exist_ok=True)

        rel_path = os.path.join(tmp_dir, "settings.json")

        data = {
            "company": {
                "name": "RelCo",
                "inn": "123456789012",
                "account": "12345678901",
                "corr_account": "98765432109",
                "bik": "123456789",
                "ownership": "ЗАО"
            }
        }

        with open(rel_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        sm = settings_manager(os.path.join("..", "src", "data", "settings.json"))
        result = sm.load()

        assert result
        assert sm.company.name == "RelCo"
        assert sm.settings.company.inn == "123456789012"

        os.remove(rel_path)

    def test_load_settings_from_project_root(self):
        sm = settings_manager("settings.json")
        result = sm.load()
        assert result
        assert sm.settings.company.name != ""

    def test_load_with_parent_relative_path(self):
        sm = settings_manager("../settings.json")
        result = sm.load()
        assert result
        assert sm.settings.company.name != ""

    def test_file_name_setter_none_or_empty(self):
        sm = settings_manager("settings.json")
        sm.file_name = None
        assert os.path.basename(sm.file_name) == "settings.json"

    def test_load_without_company_key(self):
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump({"wrong_key": {}}, f, ensure_ascii=False)

        sm = settings_manager(tmp_path)
        assert not sm.load()

        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
