"""
Загружает и хранит настройки приложения
"""
import os, json
from datetime import date
from src.models.settings_model import settings_model
from typing import Optional

"""
Менеджер настроек (Singleton)
Управляет загрузкой и хранением конфигурации приложения
"""
class settings_manager:
    _instance = None
    __settings: settings_model | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_name: str = "", config_path: str = "settings.json") -> None:
        self.config_path = config_path
        if file_name:
            self.file_name = file_name

    """ Возвращает текущие настройки """
    @property
    def settings(self) -> settings_model | None:
        return self.__settings

    """ Возвращает путь к файлу настроек """
    @property
    def file_name(self) -> str:
        return getattr(self, "_settings_file", "")

    """ Устанавливает путь к файлу настроек """
    @file_name.setter
    def file_name(self, value: str):
        v = value.strip()
        if os.path.isfile(v):
            self._settings_file = v

    def load_settings(self) -> settings_model:
        if not os.path.exists(self.config_path):
            self.__settings = settings_model()
            self.save_settings()
            return self.__settings
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.__settings = settings_model.from_dict(data)
        return self.__settings

    def save_settings(self) -> None:
        if not self.__settings:
            self.__settings = settings_model()
        data = self.__settings.to_dict()
        os.makedirs(os.path.dirname(self.config_path) or ".", exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def set_block_period(self, block_date: date) -> None:
        if not self.__settings:
            self.load_settings()
        self.__settings.block_period = block_date
        self.save_settings()

    def get_block_period(self) -> Optional[date]:
        if not self.__settings:
            self.load_settings()
        return self.__settings.block_period
