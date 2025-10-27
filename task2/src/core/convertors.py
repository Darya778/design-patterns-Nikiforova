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
    def convert(self, obj: any):
        if isinstance(obj, (int, float, str, bool)):
            return obj
        raise TypeError(f"Unsupported type for basic_convertor: {type(obj)}")


"""
Конвертор для объектов datetime
Возвращает ISO-строку
"""
class datetime_convertor(abstract_covertor):
    def convert(self, obj: any):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Unsupported type for datetime_convertor: {type(obj)}")


"""
Конвертор для ссылочных объектов (Reference)
"""
class reference_convertor(abstract_covertor):
    def convert(self, obj: any) -> dict:
        from src.logics.convert_factory import convert_factory
        factory = convert_factory()
        result = {}

        for attr, value in vars(obj).items():
            clean_name = attr.split("__")[-1] if "__" in attr else attr

            if callable(value):
                continue

            result[clean_name] = factory.convert(value)

        return result
