from dataclasses import is_dataclass, asdict
from datetime import date, datetime
from typing import Any

class Serializer:
    """Универсальный сериализатор доменных моделей в JSON-ready структуры."""

    @staticmethod
    def to_dict(obj: Any) -> Any:
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            return obj.to_dict()

        if is_dataclass(obj):
            d = asdict(obj)
            for k, v in d.items():
                if isinstance(v, (date, datetime)):
                    d[k] = v.isoformat()
            return d

        if isinstance(obj, dict):
            return {k: Serializer.to_dict(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [Serializer.to_dict(i) for i in obj]

        return obj

    @staticmethod
    def dump_jsonable(data: Any) -> Any:
        return Serializer.to_dict(data)
