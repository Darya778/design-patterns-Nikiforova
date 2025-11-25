"""
Модель настроек приложения (domain model)
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any
from enum import Enum
from src.models.company_model import company_model
from src.core.validator import validator

class ResponseFormat(Enum):
    CSV = "CSV"
    Markdown = "md"
    JSON = "JSON"
    XML = "XML"

@dataclass
class settings_model:
    """
    Domain-модель настроек приложения.
    """
    data_source: str = ""
    response_format: ResponseFormat = ResponseFormat.JSON
    company: Optional[company_model] = None
    block_period: Optional[date] = None

    """ Устанавливает текущую компанию с проверкой валидности """
    def set_company(self, company_obj: company_model):
        validator.validate(company_obj, company_model)
        self.company = company_obj

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data_source": self.data_source,
            "response_format": self.response_format.name if self.response_format else None,
            "company": self.company.to_dict() if self.company and hasattr(self.company, "to_dict") else None,
            "block_period": self.block_period.isoformat() if self.block_period else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "settings_model":
        rf = data.get("response_format", "JSON")
        try:
            response_format = ResponseFormat[rf.upper()]
        except Exception:
            response_format = ResponseFormat.JSON
        bp = data.get("block_period")
        bp_date = date.fromisoformat(bp) if bp else None
        return cls(
            data_source=data.get("data_source", ""),
            response_format=response_format,
            company=None,
            block_period=bp_date
        )

    def __repr__(self):
        return f"<settings_model(data_source={self.data_source}, response_format={self.response_format}, block_period={self.block_period})>"
