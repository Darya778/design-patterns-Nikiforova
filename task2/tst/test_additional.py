import os
import json
import tempfile
import unittest

from src.core.abstract_reference import abstract_reference
from src.core.validator import validator, argument_exception, operation_exception, error_proxy
from src.models.company_model import company_model
from src.models.nomenclature_model import nomenclature_model
from src.models.group_model import group_model
from src.models.unit_model import unit_model
from src.models.organization_model import organization_model
from src.settings_manager import settings_manager

"""Вспомогательный класс для тестирования abstract_reference"""
class dummy_reference(abstract_reference):
    pass


class test_abstract_reference(unittest.TestCase):
    def test_success_set_unique_code_manual(self):
        """
        Проверка успешного изменения unique_code вручную
        Ожидание: после присвоения значение unique_code обновляется
        """
        obj = dummy_reference("A")
        obj.unique_code = "manual_code"
        self.assertEqual(obj.unique_code, "manual_code")

    def test_success_equality_same_unique_code(self):
        """
        Проверка равенства объектов по одинаковому unique_code
        Ожидание: объекты считаются равными, если unique_code совпадает
        """
        obj1 = dummy_reference("A")
        obj2 = dummy_reference("B")
        obj2.unique_code = obj1.unique_code
        self.assertEqual(obj1, obj2)


class test_validator(unittest.TestCase):
    def test_error_validate_none(self):
        """
        Проверка ошибки при передаче None в validator.validate
        Ожидание: возбуждается argument_exception
        """
        with self.assertRaises(argument_exception):
            validator.validate(None, str)

    def test_error_validate_empty_string(self):
        """
        Проверка ошибки при передаче пустой строки
        Ожидание: возбуждается argument_exception
        """
        with self.assertRaises(argument_exception):
            validator.validate("   ", str)

    def test_error_validate_exceeds_max_length(self):
        """
        Проверка ошибки при строке, превышающей max_length
        Ожидание: возбуждается argument_exception
        """
        with self.assertRaises(argument_exception):
            validator.validate("X" * 51, str, max_length=50)

    def test_error_error_proxy_wrap_exception(self):
        """
        Проверка трансформации исключений с помощью error_proxy.wrap
        Ожидание: исходный Exception преобразуется в operation_exception
        """
        @error_proxy.wrap()
        def faulty():
            raise Exception("original")
        with self.assertRaises(operation_exception):
            faulty()


class test_company_model_additional(unittest.TestCase):
    def set_up(self):
        self.c = company_model(name="Test")

    def test_error_set_account_too_short(self):
        """
        Проверка ошибки при установке account длиной < 11
        """
        with self.assertRaises(ValueError):
            self.c.account = "123"

    def test_error_set_corr_account_too_short(self):
        """
        Проверка ошибки при установке corr_account длиной < 11
        """
        with self.assertRaises(ValueError):
            self.c.corr_account = "12"

    def test_error_set_bik_too_short(self):
        """
        Проверка ошибки при установке bik длиной < 9
        """
        with self.assertRaises(ValueError):
            self.c.bik = "123"

    def test_error_set_ownership_too_long(self):
        """
        Проверка ошибки при установке ownership длиной > 5
        """
        with self.assertRaises(ValueError):
            self.c.ownership = "СЛИШКОМДЛИННО"


class test_nomenclature_model_additional(unittest.TestCase):
    def test_error_set_full_name_empty_string(self):
        """
        Проверка ошибки при присвоении пустой строки full_name
        Ожидание: возбуждается argument_exception
        """
        g = group_model("Овощи")
        u = unit_model("кг", 1000, unit_model("грамм", 1))
        n = nomenclature_model(name="Морковь", full_name="Морковь молодая", group=g, unit=u)
        with self.assertRaises(argument_exception):
            n.full_name = "   "

    def test_success_init_without_unit(self):
        """
        Проверка инициализации nomenclature_model без unit
        Ожидание: свойство unit остаётся None
        """
        g = group_model("Овощи")
        n = nomenclature_model(name="Морковь", full_name="Морковь", group=g, unit=None)
        self.assertIsNone(n.unit)


class test_organization_model_additional(unittest.TestCase):
    def set_up(self):
        self.org = organization_model()

    def test_setters_valid_and_invalid_values(self):
        """
        Проверка работы сеттеров OrganizationModel
        Ожидание: корректные значения устанавливаются, некорректные - вызывают argument_exception
        """
        # inn
        self.org.inn = "123456789012"
        self.assertEqual(self.org.inn, "123456789012")
        with self.assertRaises(argument_exception):
            self.org.inn = "123"

        # account
        self.org.account = "12345678901"
        self.assertEqual(self.org.account, "12345678901")
        with self.assertRaises(argument_exception):
            self.org.account = "123"

        # corr_account
        self.org.corr_account = "98765432109"
        self.assertEqual(self.org.corr_account, "98765432109")
        with self.assertRaises(argument_exception):
            self.org.corr_account = "98"

        # bik
        self.org.bik = "123456789"
        self.assertEqual(self.org.bik, "123456789")
        with self.assertRaises(argument_exception):
            self.org.bik = "123"

        # ownership
        self.org.ownership = "ООО"
        self.assertEqual(self.org.ownership, "ООО")
        # длинное значение тоже допустимо
        self.org.ownership = "TOO_LONG"
        self.assertEqual(self.org.ownership, "TOO_LONG")


class test_unit_model_additional(unittest.TestCase):
    def test_error_create_unit_factor_leq_zero(self):
        """
        Проверка ошибки при создании unit_model с factor <= 0
        Ожидание: возбуждается argument_exception
        """
        with self.assertRaises(argument_exception):
            unit_model("bad", 0)

    def test_success_to_base_without_base_unit(self):
        """
        Проверка метода to_base без base_unit
        Ожидание: возвращается исходное значение без преобразования
        """
        u = unit_model("шт", 1)
        self.assertEqual(u.to_base(10), 10)

    def test_success_from_base_without_base_unit(self):
        """
        Проверка метода from_base без base_unit
        Ожидание: возвращается исходное значение без преобразования
        """
        u = unit_model("шт", 1)
        self.assertEqual(u.from_base(10), 10)

    def test_equality_and_repr(self):
        """
        Проверка работы __eq__ и __repr__ у unit_model
        Ожидание: разные объекты не равны, объект равен сам себе, repr содержит имя класса
        """
        g = unit_model("грамм", 1)
        k1 = unit_model("кг", 1000, g)
        k2 = unit_model("кг", 1000, g)
        self.assertNotEqual(k1, k2)
        self.assertEqual(k1, k1)
        self.assertIn("unit_model", repr(k1))


class test_settings_manager_additional(unittest.TestCase):
    def test_file_name_setter_empty_string_ignored(self):
        """
        Проверка установки пустого пути в file_name
        Ожидание: свойство file_name не изменяется
        """
        sm = settings_manager("settings.json")
        old_file = sm.file_name
        sm.file_name = "   "
        self.assertEqual(sm.file_name, old_file)

    def test_load_file_without_company_returns_false(self):
        """
        Проверка загрузки JSON без ключа company
        Ожидание: метод load возвращает False
        """
        tmp_fd, tmp_path = tempfile.mkstemp()
        os.close(tmp_fd)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump({"not_company": {}}, f, ensure_ascii=False)

        sm = settings_manager(tmp_path)
        self.assertFalse(sm.load())
        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
