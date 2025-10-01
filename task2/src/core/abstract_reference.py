"""
Базовый абстрактный класс для справочных сущностей
"""

from abc import ABC
import uuid
from src.core.validator import validator, argument_exception

"""
Базовый абстрактный класс модели
Содержит уникальный код и перегрузку сравнения
"""
class abstract_model(ABC):

    __unique_code: str

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    """ Уникальный код модели """
    @property
    def unique_code(self) -> str:
        return self.__unique_code

    """ Устанавливает уникальный код """
    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()

    """ Перегрузка сравнения по уникальному коду """
    def __eq__(self, value: str) -> bool:
        return self.__unique_code == value


"""
Абстрактный класс для справочных сущностей с общим полем name
Ограничение: длина name не более 50 символов
"""
class abstract_reference(abstract_model):

    __name: str = ""

    def __init__(self, name: str = "") -> None:
        """
        Инициализация справочной модели
        Args:
            name: наименование (строка до 50 символов)
        """
        super().__init__()
        if name:
            self.name = name

    """ Наименование (строка до 50 символов) """
    @property
    def name(self) -> str:
        return self.__name

    """ Устанавливает наименование с проверкой длины (<=50) """
    @name.setter
    def name(self, value: str):
        try:
            validator.validate(value, str, max_length=50)
        except argument_exception as ex:
            raise
        self.__name = value.strip()
