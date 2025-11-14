from src.models.filter_dto import FilterDTO

def get_nested_value(obj, field_path):
    """
    Извлекает значение из вложенных структур
    - из объектов через getattr
    - из словарей через dict[key]
    - из вложенных структур
    """
    parts = field_path.split(".")

    current = obj

    for part in parts:
        if current is None:
            return None

        if isinstance(current, dict):
            current = current.get(part)
            continue

        if hasattr(current, part):
            current = getattr(current, part)
            continue

        if isinstance(current, dict):
            for key in current.keys():
                if key.lower() == part.lower():
                    current = current[key]
                    break
            else:
                return None
            continue

        return None

    return current


def filter_objects(objects, filters):
    """
    Фильтрует список объектов по заданным критериям
    Поддерживает вложенные поля и разные типы сравнения
    """
    result = objects

    for f in filters:
        filtered = []

        for obj in result:
            value = get_nested_value(obj, f.field_name)
            if value is None:
                continue

            value_str = str(value).lower()
            filter_str = str(f.value).lower()

            if f.filter_type == "EQUALS":
                if value_str == filter_str:
                    filtered.append(obj)

            elif f.filter_type == "LIKE":
                if filter_str in value_str:
                    filtered.append(obj)

        result = filtered

    return result
