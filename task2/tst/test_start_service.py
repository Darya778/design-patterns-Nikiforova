# -*- coding: utf-8 -*-
"""
Тест: test_start_service
Назначение: проверка создания базовых данных сервисом start_service
"""

import unittest
from src.core.storage_repository import storage_repository
from src.start_service import start_service


class TestStartService(unittest.TestCase):
    """Юнит-тесты для проверки формирования данных сервисом start_service"""

    def setUp(self):
        """Подготовка данных перед выполнением каждого теста"""
        self.repo = storage_repository()
        self.service = start_service(self.repo)
        self.service.create()

    def test_should_create_nomenclature_data(self):
        """Проверяет, что данные по номенклатуре были созданы"""
        self.assertGreater(len(self.repo.nomenclatures), 0, "Номенклатура не была создана")

    def test_should_create_units_data(self):
        """Проверяет, что данные по единицам измерения были созданы"""
        self.assertGreater(len(self.repo.units), 0, "Единицы измерения не были созданы")

    def test_should_create_groups_data(self):
        """Проверяет, что данные по группам были созданы"""
        self.assertGreater(len(self.repo.groups), 0, "Группы не были созданы")

    def test_should_create_receipts_data(self):
        """Проверяет, что данные по рецептам были созданы"""
        self.assertGreater(len(self.repo.receipts), 0, "Рецепты не были созданы")


if __name__ == "__main__":
    unittest.main()
