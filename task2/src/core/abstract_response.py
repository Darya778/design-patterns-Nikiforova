import abc
from src.core.validator import validator, operation_exception

""" Абстрактный класс для формирования ответов в различных форматах """
class abstract_response(abc.ABC):
  
    """ Абстрактный метод, который должен быть реализован в каждом потомке """
    @abc.abstractmethod
    def create_response(self, data: list[dict]) -> str:

        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Нет данных!")
        return ""
