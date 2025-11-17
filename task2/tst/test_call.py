import requests
import json
import os

BASE = "http://127.0.0.1:8080"
OUT_DIR = "../data_out"
os.makedirs(OUT_DIR, exist_ok=True)

def test_filter_nomenclature():
    """Тест фильтрации номенклатуры через REST API"""

    response = requests.post(
        f"{BASE}/api/filter/nomenclature",
        json=[
            {"field_name": "name", "value": "Мо", "filter_type": "LIKE"}
        ]
    )

    data = response.json()

    output_file = os.path.join(OUT_DIR, "filter_nomenclature.json")
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def test_filter_osv():
    """Тест фильтрации ОСВ через REST API"""

    response = requests.post(
        f"{BASE}/api/report/osv/filter",
        json={
            "start": "1900-01-01",
            "end":   "2100-01-01",
            "warehouse": None,
            "filters": [
                {
                    "field_name": "Номенклатура.name",
                    "value": "Мо",
                    "filter_type": "LIKE"
                }
            ]
        }
    )

    data = response.json()

    output_file = os.path.join(OUT_DIR, "filter_osv.json")
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    test_filter_nomenclature()
    test_filter_osv()
