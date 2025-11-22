"""
Загружает и хранит настройки приложения
"""

import os
import json
from datetime import date
from src.models.settings_model import settings_model, ResponseFormat
from src.models.company_model import company_model
from dataclasses import dataclass
from datetime import date
from enum import Enum

"""
Менеджер настроек (Singleton)
Управляет загрузкой и хранением конфигурации приложения
"""
class settings_manager:

    _instance = None
    __settings: settings_model | None = None
    __file_name: str = ""

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_name: str = "", config_path: str = "settings.json"):
        self.config_path = config_path
        if file_name:
            self.file_name = file_name

    """ Возвращает текущие настройки """
    @property
    def settings(self) -> settings_model | None:
        return self.__settings

    """ Возвращает текущую организацию """
    @property
    def company(self) -> company_model | None:
        return self.__settings.company if self.__settings else None

    """ Возвращает путь к файлу настроек """
    @property
    def file_name(self) -> str:
        return getattr(self, "_settings_file", "")

    """ Устанавливает путь к файлу настроек """
    @file_name.setter
    def file_name(self, value: str):
        value = value.strip()
        if os.path.isfile(value):
            self._settings_file = value

    def save_settings(self):
        """
        Сохраняем всю модель settings
        """
        if not self.__settings:
            self.__settings = settings_model()

        data = {
            "data_source": self.__settings.data_source,
            "response_format": self.__settings.response_format.name,
            "block_period": self.__settings.block_period.isoformat()
            if self.__settings.block_period else None
        }

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def set_block_period(self, block_date: date):
        if not self.__settings:
            self.load_settings()

        self.__settings.block_period = block_date
        self.save_settings()

    def get_block_period(self) -> date | None:
        if not self.__settings:
            self.load_settings()
        return self.__settings.block_period

    """ Загружает настройки из файла """
    def load(self) -> bool:
        if not self.__file_name:
            raise FileNotFoundError("Не указан путь к файлу настроек")

        if not os.path.isfile(self.__file_name):
            raise FileNotFoundError(f"Файл {self.__file_name} не найден")

        try:
            with open(self.__file_name, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict) and "company" in data:
                comp = self._dict_to_company(data["company"])
                self.__settings = settings_model(company=comp)
                return True
            return False
        except Exception as ex:
            print("Ошибка загрузки:", ex)
            return False

    """ Создает экземпляр company_model из словаря """
    def _dict_to_company(self, data: dict) -> company_model:
        comp = company_model()
        for field in ("name", "inn", "account", "corr_account", "bik", "ownership"):
            if field in data and data[field]:
                setattr(comp, field, data[field])
        return comp

    """ Настройки по умолчанию """
    def default(self):
        comp = company_model()
        comp.name = "Рога и копыта"
        self.__settings = settings_model(company=comp)

    def load_settings(self) -> settings_model:
        """
        Чтение полной модели из JSON
        """
        if not os.path.exists(self.config_path):
            self.__settings = settings_model()
            self.save_settings()
            return self.__settings

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        response_format = ResponseFormat[data.get("response_format", "JSON").upper()]
        block_str = data.get("block_period", None)
        block_date = date.fromisoformat(block_str) if block_str else None

        self.__settings = settings_model(
            data_source=data.get("data_source", ""),
            response_format=response_format,
            block_period=block_date
        )

        return self.__settings
