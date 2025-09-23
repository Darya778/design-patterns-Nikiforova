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
        if value is None:
            return
        value = value.strip()
        if value == "":
            return
        norm = os.path.normpath(value)
        if not os.path.isabs(norm):
            norm = os.path.abspath(norm)
        if os.path.exists(norm):
            self.__file_name = norm

    def load(self):
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настройки")

        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if "company" in data.keys():
                item = data["company"]
                name = item.get("name", "")
                if name:
                    self.__company.name = name
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
        name = data.get("name", "")
        inn = data.get("inn", "")
        account = data.get("account", "")
        corr_account = data.get("corr_account", "")
        bik = data.get("bik", "")
        ownership = data.get("ownership", "")

        comp = company_model()
        if name and name.strip() != "":
            comp.name = name
        if inn != "":
            comp.inn = inn
        if account != "":
            comp.account = account
        if corr_account != "":
            comp.corr_account = corr_account
        if bik != "":
            comp.bik = bik
        if ownership != "":
            comp.ownership = ownership

        return Settings(company=comp)

