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
            candidate = os.path.abspath(norm)
            if os.path.exists(candidate):
                self.__file_name = candidate
                return

            candidate = os.path.abspath(os.path.join(os.getcwd(), "..", os.path.basename(norm)))
            if os.path.exists(candidate):
                self.__file_name = candidate
                return

            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            candidate = os.path.join(project_root, norm)
            if os.path.exists(candidate):
                self.__file_name = candidate
                return

        if os.path.isabs(norm) and os.path.exists(norm):
            self.__file_name = norm

    def load(self):
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настройки")

        if not os.path.exists(self.__file_name):
            raise FileNotFoundError(f"Файл {self.__file_name} не найден")

        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if "company" in data.keys():
                item = data["company"]
                self.__company.name = item.get("name", self.__company.name)
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
        comp = company_model()
        if data.get("name"):
            comp.name = data["name"]
        if data.get("inn"):
            comp.inn = data["inn"]
        if data.get("account"):
            comp.account = data["account"]
        if data.get("corr_account"):
            comp.corr_account = data["corr_account"]
        if data.get("bik"):
            comp.bik = data["bik"]
        if data.get("ownership"):
            comp.ownership = data["ownership"]

        return Settings(company=comp)
