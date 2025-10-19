import csv
import io
import json
import xml.etree.ElementTree as ET

""" Форматирование данных в CSV (comma-separated values) """
class CsvFormatter:
    """
    Преобразует список словарей в CSV-таблицу
    Аргументы: data (list[dict]): Список строк с данными
    Возвращает: str: CSV-представление данных
    """
    def format(self, data: list[dict]) -> str:
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

""" Форматирование данных в JSON """
class JsonFormatter:

    """
    Преобразует список словарей в JSON-строку
    """
    def format(self, data: list[dict]) -> str:
        return json.dumps(data, indent=4, ensure_ascii=False)

""" Форматирование данных в Markdown-таблицу """
class MarkdownFormatter:

    """
    Преобразует список словарей в Markdown-таблицу
    """
    def format(self, data: list[dict]) -> str:
        if not data:
            return ""
        headers = list(data[0].keys())
        md = "| " + " | ".join(headers) + " |\n"
        md += "| " + " | ".join("---" for _ in headers) + " |\n"
        for row in data:
            md += "| " + " | ".join(str(row[h]) for h in headers) + " |\n"
        return md

""" Форматирование данных в XML """
class XmlFormatter:

    """
    Преобразует список словарей в XML-документ
    """
    def format(self, data: list[dict]) -> str:
        root = ET.Element("Items")
        for row in data:
            item = ET.SubElement(root, "Item")
            for k, v in row.items():
                elem = ET.SubElement(item, k)
                elem.text = str(v)
        return ET.tostring(root, encoding="unicode")
