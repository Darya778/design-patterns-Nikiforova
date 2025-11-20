import unicodedata


class FilterUtils:
    FIELD_ALIASES = {
        "номенклатура": "",
        "склад": "",
        "единица": "",
        "наименование": "name",
        "код": "code",
        "приход": "Приход",
        "расход": "Расход",
        "конечныйостаток": "Конечный остаток",
    }

    @staticmethod
    def normalize(s: str) -> str:
        if not isinstance(s, str):
            return s
        return unicodedata.normalize("NFKC", s).strip().lower()

    @staticmethod
    def get_nested_value(obj, field_path):
        """
        Извлекает значение из вложенных объектов/словрей
        """
        parts = field_path.split(".")
        current = obj

        for part in parts:
            part_norm = FilterUtils.normalize(part)

            if part_norm in FilterUtils.FIELD_ALIASES:
                alias = FilterUtils.FIELD_ALIASES[part_norm]

                if alias == "":
                    for key in current.keys():
                        if FilterUtils.normalize(key) == part_norm:
                            current = current[key]
                            break
                    else:
                        return None
                    continue

                part_norm = FilterUtils.normalize(alias)

            if current is None:
                return None

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

            ft = f.filter_type
            ftype = ft if isinstance(ft, str) else ft.name
            ftype = ftype.upper()

            for obj in result:
                value = FilterUtils.get_nested_value(obj, f.field_name)
                if value is None:
                    continue

                val_norm = FilterUtils.normalize(str(value))
                flt_norm = FilterUtils.normalize(str(f.value))

                if ftype == "EQUALS" and val_norm == flt_norm:
                    filtered.append(obj)

                elif ftype == "LIKE" and flt_norm in val_norm:
                    filtered.append(obj)

            result = filtered

        return result

