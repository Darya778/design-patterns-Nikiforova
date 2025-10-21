from src.core.abstract_response import abstract_response
from src.logics.response_csv import response_csv
from src.logics.response_json import response_json
from src.logics.response_md import response_md
from src.logics.response_xml import response_xml
from src.core.validator import operation_exception

""" Фабрика для создания ответов в различных форматах """
class factory_entities:
    """
    Инициализация фабрики с настройками приложения
    :param settings: экземпляр settings_manager (для определения формата по умолчанию)
    """
    def __init__(self, settings):
        self.settings = settings
        self._registry = {
            "csv": response_csv,
            "json": response_json,
            "md": response_md,
            "xml": response_xml,
        }

    def create(self, fmt: str) -> abstract_response:
        fmt = fmt.lower()
        if fmt not in self._registry:
            raise operation_exception(f"No formatter registered for format: {fmt}")
        return self._registry[fmt]()

    """
    Формирует ответ в формате, указанном в настройках
    Если формат отсутствует в реестре - генерируется исключение
    """
    def create_default(self, data):
        fmt = getattr(self.settings, "response_format", "json")

        if hasattr(fmt, "value"):
            fmt_key = fmt.value.lower()
        else:
            fmt_key = str(fmt).lower()

        if fmt_key not in self._registry:
            raise operation_exception(f"No formatter registered for format: {fmt_key}")

        formatter = self._registry[fmt_key]()
        return formatter.create_response(data)
