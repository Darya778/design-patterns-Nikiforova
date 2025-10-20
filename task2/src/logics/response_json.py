from src.core.abstract_response import abstract_response
import json

"""
Формирование ответа в формате JSON
"""
class response_json(abstract_response):
    def create_response(self, data: list[dict]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4)
