from str.models.company_model import company_model
import os
import json

class settings_manager:
    __file_name:str = ""
    __company:company_model = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self, file_name:str):
        self.file_name = file_name
        self.default()

    @property
    def company(self) -> company_model:
        return self.__company

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value:str):
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

                self.__company.name = item["name"]
                return True
            return False
        except:
            return False

    def default(self):
        self.__company = company_model()
        self.__company.name = "Рога и копыта"
