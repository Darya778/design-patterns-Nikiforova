from ..models.settings_model import SettingsModel, ResponseFormat
from .response_formatters import CsvFormatter, JsonFormatter, MarkdownFormatter, XmlFormatter

""" Фабрика для создания ответов в различных форматах """
class FactoryEntities:
    def __init__(self, settings: SettingsModel):
        self.settings = settings

    """ 
    Формирует выходной ответ в формате, определённом в настройках
    Аргументы:
        data (list[dict]): Список словарей с данными
    Возвращает:
        str: Данные, преобразованные в нужный формат
    """
    def create_default(self, data):
        fmt = self.settings.response_format

        if fmt == ResponseFormat.CSV:
            return CsvFormatter().format(data)
        elif fmt == ResponseFormat.JSON:
            return JsonFormatter().format(data)
        elif fmt == ResponseFormat.Markdown:
            return MarkdownFormatter().format(data)
        elif fmt == ResponseFormat.XML:
            return XmlFormatter().format(data)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
