from src.core.validator import validator, argument_exception

"""
Domain-модель компании
Содержит основные реквизиты: ИНН, счета, БИК, форму собственности и название
Все поля валидируются согласно правилам в _validators
"""
class company_model:
    _validators = {
        "inn": {"type": str, "digit": True, "length": 12, "error": "ИНН должен содержать 12 цифр"},
        "account": {"type": str, "digit": True, "length": 11, "error": "Счет должен содержать 11 цифр"},
        "corr_account": {"type": str, "digit": True, "length": 11, "error": "Корр. счет должен содержать 11 цифр"},
        "bik": {"type": str, "digit": True, "length": 9, "error": "БИК должен содержать 9 цифр"},
        "ownership": {"type": str, "max_length": 5, "error": "Вид собственности <= 5 символов"},
        "name": {"type": str, "strip": True, "error": "Название компании не должно быть пустым"},
    }

    """
    Конструктор модели
    Инициализирует все поля пустыми строками, далее присваивает значения из kwargs
    """
    def __init__(self, **kwargs):
        self._data = {key: "" for key in self._validators}
        for key, value in kwargs.items():
            if key in self._validators:
                setattr(self, key, value)

    """ Проверяет корректность значения по правилам из _validators """
    def _validate(self, field, value):
        rules = self._validators[field]

        if rules.get("strip") and isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return self._data.get(field, "")
            value = stripped

        try:
            validator.validate(value, rules["type"], rules.get("length") or rules.get("max_length"))
        except argument_exception as ex:
            raise ValueError(str(ex)) from ex

        if rules.get("digit") and not value.isdigit():
            raise ValueError(rules["error"])
        if rules.get("length") and len(value) != rules["length"]:
            raise ValueError(rules["error"])
        if rules.get("max_length") and len(value) > rules["max_length"]:
            raise ValueError(rules["error"])

        return value

    """ Доступ к значениям через атрибуты """
    def __getattr__(self, item):
        if item in self._validators:
            return self._data[item]
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")

    """ Присвоение значения атрибуту с автоматической валидацией """
    def __setattr__(self, key, value):
        if key in ("_data", "_validators"):
            super().__setattr__(key, value)
        elif key in self._validators:
            self._data[key] = self._validate(key, value)
        else:
            raise AttributeError(f"Неизвестное поле: {key}")

    """ Сравнение двух моделей компании """
    def __eq__(self, other):
        return isinstance(other, company_model) and self._data == other._data

    """ Отладочное представление объекта """
    def __repr__(self):
        return f"company_model(name='{self._data['name']}', inn='{self._data['inn']}')"

