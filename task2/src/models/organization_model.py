"""
Модель организации: поля ИНН, БИК, счет, форма собственности
Конструктор поддерживает инициализацию из settings_model (копирование полей)
"""

from typing import Optional
from src.core.abstract_reference import abstract_reference
from src.core.validator import validator, argument_exception
from src.models.company_model import company_model
from src.models.settings_model import settings_model

""" Организация - справочная сущность, хранит финансовые реквизиты """
class organization_model(abstract_reference):

    __inn: str = ""
    __bik: str = ""
    __account: str = ""
    __corr_account: str = ""
    __ownership: str = ""

    """
    Инициализация организации
    Args:
        name: наименование (<=50 символов)
        inn, bik, account, corr_account, ownership: реквизиты (строки)
        settings: settings_model - при передаче, реквизиты копируются из settings.company
    """
    def __init__(self, name: str = "", inn: str = "", bik: str = "",
                 account: str = "", corr_account: str = "", ownership: str = "",
                 settings: Optional[settings_model] = None):

        if settings is not None:
            if not isinstance(settings, settings_model):
                raise argument_exception("settings должен быть экземпляром settings_model")
            if settings.company is None:
                raise argument_exception("settings.company пуст")
            company_obj = settings.company
            inn = getattr(company_obj, "inn", inn)
            bik = getattr(company_obj, "bik", bik)
            account = getattr(company_obj, "account", account)
            corr_account = getattr(company_obj, "corr_account", corr_account)
            ownership = getattr(company_obj, "ownership", ownership)
            name = getattr(company_obj, "name", name)

        if inn:
            self.inn = inn
        if bik:
            self.bik = bik
        if account:
            self.account = account
        if corr_account:
            self.corr_account = corr_account
        if ownership:
            self.ownership = ownership
        if name:
            self.name = name
        super().__init__(name)


    """ ИНН организации (строка из цифр, 12 символов) """
    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        validator.validate(value, str)
        if not value.isdigit() or len(value) != 12:
            raise argument_exception("ИНН должен содержать 12 цифр")
        self.__inn = value.strip()

    """ Расчётный счёт (11 цифр) """
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        validator.validate(value, str)
        if not value.isdigit() or len(value) != 11:
            raise argument_exception("Счет должен содержать 11 цифр")
        self.__account = value.strip()

    """ Корреспондентский счёт (11 цифр) """
    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        validator.validate(value, str)
        if not value.isdigit() or len(value) != 11:
            raise argument_exception("Корреспондентский счет должен содержать 11 цифр")
        self.__corr_account = value.strip()

    """ БИК (9 цифр) """
    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        validator.validate(value, str)
        if not value.isdigit() or len(value) != 9:
            raise argument_exception("БИК должен содержать 9 цифр")
        self.__bik = value.strip()

    """ Форма собственности (строка, без ограничения) """
    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        validator.validate(value, str)
        if len(value.strip()) > 50:
            raise argument_exception("ownership - слишком длинная строка")
        self.__ownership = value.strip()
