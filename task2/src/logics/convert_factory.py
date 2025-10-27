from datetime import datetime
from collections import OrderedDict
from src.core.convertors import basic_convertor, datetime_convertor, reference_convertor


class convert_factory:
    """
    Универсальная фабрика для конвертации объектов разных типов в словари.
    Реализует рекурсивную обработку и сортировку ключей для читаемого JSON.
    """
    def __init__(self):
        self._registry = {
            "basic": basic_convertor(),
            "datetime": datetime_convertor(),
            "reference": reference_convertor()
        }

        self._preferred_order = [
            "code", "unique_code", "name", "group", "author",
            "unit", "portions", "ingredients", "steps"
        ]

    def convert(self, obj: any):
        if obj is None:
            return None

        if isinstance(obj, (int, float, str, bool)):
            return self._registry["basic"].convert(obj)

        if isinstance(obj, datetime):
            return self._registry["datetime"].convert(obj)

        if isinstance(obj, list):
            return [self.convert(i) for i in obj]

        if isinstance(obj, dict):
            data = {k: self.convert(v) for k, v in obj.items()}
            return self._sort_keys(data)

        if hasattr(obj, "code") or hasattr(obj, "id") or hasattr(obj, "__class__"):
            data = self._registry["reference"].convert(obj)
            return self._sort_keys(data)

        if hasattr(obj, "__dict__"):
            data = {k: self.convert(v) for k, v in vars(obj).items()}
            return self._sort_keys(data)

        return str(obj)

    def _sort_keys(self, data: dict) -> dict:
        """
        Упорядочивает словарь по логике бизнес-объекта:
        сначала ключи из _preferred_order, потом остальные.
        """
        ordered = OrderedDict()
        for key in self._preferred_order:
            if key in data:
                ordered[key] = data[key]

        for k, v in data.items():
            if k not in ordered:
                ordered[k] = v

        return ordered

    def convert_collection(self, items: list):
        return [self.convert(i) for i in items]
