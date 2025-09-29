import os
import json
import tempfile
import unittest
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.warehouse_model import warehouse_model
from src.models.settings_model import settings_model
from src.settings_manager import settings_manager
from src.core.validator import argument_exception

class test_unit_model(unittest.TestCase):

    def test_success_create_units_base_and_derived(self):
        """
        Проверка создания базовой и производной единиц измерения
        Входные данные: базовая "грамм" (factor=1), производная "кг" (factor=1000)
        Ожидание: корректный пересчет при to_base и from_base
        """
        base = unit_model("грамм", 1)
        kilo = unit_model("кг", 1000, base)
        self.assertEqual(base.factor, 1)
        self.assertEqual(kilo.factor, 1000)
        self.assertEqual(kilo.to_base(2), 2000)
        self.assertEqual(kilo.from_base(2000), 2.0)

    def test_error_create_unit_factor_leq_zero(self):
        """
        Проверка ошибки при создании единицы измерения с factor <= 0
        Ожидание: возбуждается argument_exception
        """
        with self.assertRaises(argument_exception):
            unit_model("bad", 0)


class test_nomenclature_and_group(unittest.TestCase):

    def test_success_create_nomenclature_with_group_and_unit(self):
        """
        Проверка создания номенклатуры с группой и единицей измерения
        Ожидание: свойства group и unit корректно устанавливаются
        """
        g = group_model("Овощи")
        u = unit_model("кг", 1000, unit_model("грамм", 1))
        n = nomenclature_model(name="Морковь", full_name="Морковь молодой фасованная", group=g, unit=u)
        self.assertEqual(n.name, "Морковь")
        self.assertEqual(n.full_name, "Морковь молодой фасованная")
        self.assertIs(n.group, g)
        self.assertIs(n.unit, u)


class test_organization_from_settings(unittest.TestCase):

    def test_success_create_organization_from_settings_manager(self):
        """
        Проверка создания organization_model из настроек
        Входные данные: JSON с объектом company
        Ожидание: свойства organization_model совпадают с данными файла
        """
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".json")
        os.close(tmp_fd)

        data = {"company": {
            "name": "OrgFromSettings",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "98765432109",
            "bik": "123456789",
            "ownership": "ООО"
        }}
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        mgr = settings_manager(tmp_path)
        loaded = mgr.load()
        self.assertTrue(loaded)
        self.assertIsNotNone(mgr.settings)
        org = organization_model(settings=mgr.settings)
        self.assertEqual(org.name, "OrgFromSettings")
        self.assertEqual(org.inn, "123456789012")
        self.assertEqual(org.account, "12345678901")

        os.remove(tmp_path)


class test_warehouse_and_misc(unittest.TestCase):

    def test_success_create_warehouse_with_name(self):
        """
        Проверка создания склада с именем
        """
        w = warehouse_model("Основной склад")
        self.assertEqual(w.name, "Основной склад")

    def test_error_create_group_name_too_long(self):
        """
        Проверка ограничения имени справочной модели (<=50 символов)
        Ожидание: возбуждается argument_exception
        """
        long_name = "x" * 51
        with self.assertRaises(argument_exception):
            group_model(long_name)
