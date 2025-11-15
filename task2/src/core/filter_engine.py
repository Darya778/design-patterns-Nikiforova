class filter_engine:
    """
    Класс для универсальной фильтрации моделей и словарей по пути вида
    "group.name" или "Номенклатура.name"
    """

    @staticmethod
    def get_nested(obj, path: str):
        parts = path.split(".")

        for p in parts:
            if obj is None:
                return None

            if isinstance(obj, dict):
                obj = obj.get(p)
            else:
                obj = getattr(obj, p, None)

        return obj

    @staticmethod
    def match(obj, filter_dto):
        value = filter_engine.get_nested(obj, filter_dto.field_name)
        if value is None:
            return False

        value_s = str(value).lower()
        filter_s = str(filter_dto.value).lower()

        if filter_dto.filter_type.name == "EQUALS":
            return value_s == filter_s

        if filter_dto.filter_type.name == "LIKE":
            return filter_s in value_s

        return False

    @staticmethod
    def filter(objects, filters):
        result = []
        for obj in objects:
            if all(filter_engine.match(obj, f) for f in filters):
                result.append(obj)
        return result
