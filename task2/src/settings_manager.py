"""
Загружает и хранит настройки приложения из JSON-файла
"""

import os
import json
from src.models.company_model import company_model
from src.models.settings_model import settings_model
import json
from src.models.settings_model import settings_model, ResponseFormat

"""
Менеджер настроек (Singleton)
Управляет загрузкой и хранением конфигурации приложения
"""
class settings_manager:

    __file_name: str = ""
    __settings: settings_model | None = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_name: str = "", config_path: str = "settings.json"):
        if file_name:
            self.file_name = file_name
            self.config_path = config_path
            self.settings: settings_model | None = None

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
        return self.__file_name

    """ Устанавливает путь к файлу настроек """
    @file_name.setter
    def file_name(self, value: str):
        if not value:
            return
        path = os.path.normpath(value.strip())

        if os.path.isfile(path):
            self.__file_name = os.path.abspath(path)
            return

        candidates = [
            os.path.abspath(path),
            os.path.abspath(os.path.join(os.getcwd(), "..", os.path.basename(path))),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")), path),
        ]

        for candidate in candidates:
            if os.path.isfile(candidate):
                self.__file_name = candidate
                return

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

    """ Настройки по умолчанию """
    def default(self):
        comp = company_model()
        comp.name = "Рога и копыта"
        self.__settings = settings_model(company=comp)

    """ Создает экземпляр company_model из словаря """
    def _dict_to_company(self, data: dict) -> company_model:
        comp = company_model()
        for field in ("name", "inn", "account", "corr_account", "bik", "ownership"):
            if field in data and data[field]:
                setattr(comp, field, data[field])
        return comp

    """ Загружает настройки из JSON-файла """
    def load_settings(self):

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        format_str = data.get("response_format", "JSON")
        response_format = ResponseFormat[format_str.upper()]

        self.settings = settings_model(
            data_source=data.get("data_source", ""),
            response_format=response_format
        )
        return self.settings
