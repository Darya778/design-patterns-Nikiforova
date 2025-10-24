from datetime import datetime
from src.core.convertors import basic_convertor, datetime_convertor, reference_convertor

"""
Фабрика для определения подходящего конвертора и выполнения конверсии объекта
"""
class convert_factory:
    def __init__(self):
        self._basic = basic_convertor()
        self._datetime = datetime_convertor()
        self._reference = reference_convertor()

    def convert(self, obj: any) -> dict:
        """
        Определяет тип объекта и вызывает соответствующий конвертор.
        :param obj: любой объект
        :return: dict
        """

        if isinstance(obj, (int, float, str)):
            return self._basic.convert(obj)

        elif isinstance(obj, datetime):
            return self._datetime.convert(obj)

        elif hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            data = obj.to_dict()
            return {k: self._convert_value(v) for k, v in data.items()}

        elif hasattr(obj, "code") and hasattr(obj, "name"):
            return self._reference.convert(obj)

        elif isinstance(obj, dict):
            return {k: self._convert_value(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return {"items": [self._convert_value(i) for i in obj]}

        raise TypeError(f"Unsupported object type: {type(obj)}")

    def _convert_value(self, value):
        """Рекурсивная конвертация значения."""
        if isinstance(value, (int, float, str)):
            return value
        elif isinstance(value, datetime):
            return value.isoformat()
        elif hasattr(value, "to_dict"):
            return self.convert(value)
        elif hasattr(value, "code") and hasattr(value, "name"):
            return self._reference.convert(value)
        elif isinstance(value, list):
            return [self._convert_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._convert_value(v) for k, v in value.items()}
        else:
            return str(value)

    def convert_collection(self, items: list) -> list:
        """Конвертирует список объектов в список словарей."""
        return [self.convert(i) for i in items]
