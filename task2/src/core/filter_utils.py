import unicodedata


class FilterUtils:

    @staticmethod
    def normalize(s: str) -> str:
        if not isinstance(s, str):
            return s
        return unicodedata.normalize("NFKC", s).strip().lower()

    @staticmethod
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
            part_norm = FilterUtils.normalize(part)

            if current is None:
                return None

            # ---- DICT ----
            if isinstance(current, dict):
                found = False
                for key in current.keys():
                    if FilterUtils.normalize(key) == part_norm:
                        current = current[key]
                        found = True
                        break
                if not found:
                    return None
                continue

            # ---- OBJECT ----
            attrs = {
                FilterUtils.normalize(a): a
                for a in dir(current)
                if not a.startswith("_")
            }

            if part_norm in attrs:
                current = getattr(current, attrs[part_norm])
                continue

            return None

        return current

    @staticmethod
    def apply(objects, filters):
        result = objects

        for f in filters:
            filtered = []

            for obj in result:
                value = FilterUtils.get_nested_value(obj, f.field_name)
                if value is None:
                    continue

                val_norm = FilterUtils.normalize(str(value))
                flt_norm = FilterUtils.normalize(str(f.value))

                ftype = f.filter_type.name  # enum → string

                match ftype:
                    case "EQUALS":
                        if val_norm == flt_norm:
                            filtered.append(obj)

                    case "LIKE":
                        if flt_norm in val_norm:
                            filtered.append(obj)

            result = filtered

        return result
