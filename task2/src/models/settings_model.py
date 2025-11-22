"""
Модель настроек приложения
"""
from src.models.company_model import company_model
from src.core.validator import validator
from enum import Enum
from dataclasses import dataclass
from datetime import date


class ResponseFormat(Enum):
    CSV = "CSV"
    Markdown = "md"
    JSON = "JSON"
    XML = "XML"


@dataclass
class settings_model:
    """
    Domain-модель настроек приложения.
    Полная модель, хранящаяся в JSON.
    """
    data_source: str = ""
    response_format: ResponseFormat = ResponseFormat.JSON
    company: company_model | None = None
    block_period: date | None = None

    """ Устанавливает текущую компанию с проверкой валидности """
    def set_company(self, company_obj: company_model):
        validator.validate(company_obj, company_model)
        self.company = company_obj

    def __repr__(self):
        return (
            f"<settings_model("
            f"company={repr(self.company)}, "
            f"format={self.response_format.value}, "
            f"block_period={self.block_period}"
            f")>"
        )
