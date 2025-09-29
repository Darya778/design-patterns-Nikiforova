from src.core.validator import validator
from src.core.abstract_reference import abstract_model

"""
Domain-модель для представления хранилища
Наследуется от abstract_model
"""
class storage_model(abstract_model):
    __name:str = ""

    """ Возвращает имя хранилища """
    @property
    def name(self) -> str:
        return self.__name

    """ Устанавливает имя хранилища с проверкой типа """
    @name.setter
    def name(self, value:str):
        validator.validate(value, str)
        self.__name = value.strip()
