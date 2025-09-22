import os
import json
from src.models.company_model import company_model
from src.models.settings import Settings


class settings_manager:
    __file_name: str = ""
    __company: company_model = None
    __settings: Settings = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.default()

    @property
    def company(self) -> company_model:
        return self.__company

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return
        if os.path.exists(value):
            self.__file_name = value.strip()

    def load(self):
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настройки")

        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if "company" in data.keys():
                item = data["company"]
                self.__company.name = item.get("name", "")
                self.__settings = self.convert(item)
                return True
            return False
        except Exception as ex:
            print("Ошибка загрузки:", ex)
            return False

    def default(self):
        self.__company = company_model()
        self.__company.name = "Рога и копыта"
        self.__settings = None

    def convert(self, data: dict) -> Settings:
        return Settings(
            name=data.get("name", ""),
            inn=data.get("inn", "000000000000"),
            account=data.get("account", "00000000000"),
            corr_account=data.get("corr_account", "00000000000"),
            bik=data.get("bik", "000000000"),
            ownership=data.get("ownership", "00000")
        )
