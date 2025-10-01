"""
Модель настроек приложения
"""
from src.models.company_model import company_model
from src.core.validator import validator

""" Модель настроек приложения, содержащая организацию """
class settings_model:
    __company: company_model = None

    def __init__(self, company: company_model = None):
        if company is not None:
            self.company = company

    """ Текущая организация """
    @property
    def company(self) -> company_model:
        return self.__company

    """ Устанавливает организацию с проверкой валидности """
    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    def __repr__(self):
        return f"<settings_model(company={repr(self.__company)})>"
