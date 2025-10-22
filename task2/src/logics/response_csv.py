from src.core.abstract_response import abstract_response
import csv
import io

"""
Формирование ответа в формате CSV
"""
class response_csv(abstract_response):
    """
    Преобразует список словарей (данных) в CSV-формат
    Все списки внутри данных конвертируются в человекочитаемую строку через запятую
    """
    def create_response(self, data: list[dict]) -> str:
        if not data:
            return ""

        fieldnames = sorted({key for row in data for key in row.keys()})

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        formatted_data = []
        for row in data:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, list):
                    formatted_row[key] = ", ".join(map(str, value))
                else:
                    formatted_row[key] = value
            formatted_data.append(formatted_row)

        writer.writerows(formatted_data)
        return output.getvalue()
