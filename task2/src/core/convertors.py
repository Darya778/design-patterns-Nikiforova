from abc import ABC, abstractmethod
from datetime import datetime

"""
Абстрактный класс конвертора
"""
class abstract_covertor(ABC):

    @abstractmethod
    def convert(self, obj: any) -> any:
        """
        Преобразует объект в словарь или значение.
        :param obj: любой объект для конверсии
        :return: dict или простое значение
        """
        pass


"""
Конвертор для простых типов: int, float, str
Возвращает значение напрямую, чтобы JSON был читаемым
"""
class basic_convertor(abstract_covertor):
    def convert(self, obj: any) -> int | float | str:
        if isinstance(obj, (int, float, str)):
            return obj
        raise TypeError(f"Unsupported type for basic_convertor: {type(obj)}")


"""
Конвертор для объектов datetime
Возвращает ISO-строку
"""
class datetime_convertor(abstract_covertor):
    def convert(self, obj: any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Unsupported type for datetime_convertor: {type(obj)}")


"""
Конвертор для ссылочных объектов (Reference)
"""
class reference_convertor(abstract_covertor):
    def convert(self, obj: any) -> dict:
        if hasattr(obj, "code") and hasattr(obj, "name"):
            return {
                "code": getattr(obj, "code"),
                "name": getattr(obj, "name")
            }
        raise TypeError(f"Unsupported object for reference_convertor: {type(obj)}")
