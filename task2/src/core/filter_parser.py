from src.core.filters_enum import FilterType
from src.models.filter_dto import FilterDTO


class filter_parser:
    """
    Безопасный парсер входящих данных фильтра.
    Не зависит от хардкода ключей.
    """

    REQUIRED_FIELDS = {"field_name", "value", "filter_type"}

    @staticmethod
    def parse(raw_filters):
        filters = []

        if not isinstance(raw_filters, list):
            raise ValueError("filters must be list")

        for item in raw_filters:
            if not isinstance(item, dict):
                raise ValueError("Each filter must be dict")

            if not filter_parser.REQUIRED_FIELDS.issubset(item.keys()):
                raise ValueError(
                    f"Filter item missing fields. Required: {filter_parser.REQUIRED_FIELDS}"
                )

            try:
                filter_type = FilterType[item["filter_type"]]
            except KeyError:
                raise ValueError(f"Unknown filter type: {item['filter_type']}")

            filters.append(
                FilterDTO(
                    field_name=item["field_name"],
                    value=item["value"],
                    filter_type=filter_type
                )
            )

        return filters
