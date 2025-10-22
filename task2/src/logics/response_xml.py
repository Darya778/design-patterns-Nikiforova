from src.core.abstract_response import abstract_response
import xml.etree.ElementTree as ET
from xml.dom import minidom

"""
Формирование ответа в формате XML
"""
class response_xml(abstract_response):
    """
    Метод преобразует список словарей в человекочитаемый XML-документ
    Каждый элемент списка становится XML-узлом <Item>, внутри которого - поля данных
    """
    def create_response(self, data: list[dict]) -> str:
        root = ET.Element("Items")
        for row in data:
            item = ET.SubElement(root, "Item")
            for k, v in row.items():
                el = ET.SubElement(item, str(k))
                el.text = str(v)

        xml_str = ET.tostring(root, encoding="utf-8")
        dom = minidom.parseString(xml_str)
        pretty = dom.toprettyxml(indent="  ", encoding="utf-8")

        return pretty.decode("utf-8")
