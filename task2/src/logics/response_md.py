from src.core.abstract_response import abstract_response

"""
Формирование ответа в формате Markdown-таблицы
"""
class response_md(abstract_response):
    def create_response(self, data: list[dict]) -> str:
        if not data:
            return ""
        headers = list(data[0].keys())
        md = "| " + " | ".join(headers) + " |\n"
        md += "| " + " | ".join("---" for _ in headers) + " |\n"
        for row in data:
            md += "| " + " | ".join(str(row[h]) for h in headers) + " |\n"
        return md
