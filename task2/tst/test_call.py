# tst/test_call.py
import requests
import json
import os

BASE = "http://127.0.0.1:8080"
OUT_DIR = "../data_out"
os.makedirs(OUT_DIR, exist_ok=True)

def test_filter_nomenclature():
    """Тест фильтрации номенклатуры через REST API"""
    print("=== Test 1: /api/filter/nomenclature ===")

    response = requests.post(
        f"{BASE}/api/filter/nomenclature",
        json=[
            {"field_name": "name", "value": "Мо", "filter_type": "LIKE"}
        ]
    )

    print("Status:", response.status_code)
    try:
        data = response.json()
        print("Response:")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        output_file = os.path.join(OUT_DIR, "filter_nomenclature.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"[OK] Результат сохранен: {output_file}")

    except Exception:
        print(response.text)

def test_filter_osv():
    """Тест фильтрации ОСВ через REST API"""
    print("\n=== Test 2: /api/report/osv/filter ===")

    response = requests.post(
        f"{BASE}/api/report/osv/filter",
        json={
            "model_type": "nomenclature",
            "filters": [
                {
                    "field_name": "Номенклатура.name",
                    "value": "Мо",
                    "filter_type": "LIKE"
                }
            ]
        }
    )

    print("Status:", response.status_code)
    try:
        data = response.json()
        print("Response:")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        output_file = os.path.join(OUT_DIR, "filter_osv.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"[OK] Результат сохранен: {output_file}")

    except Exception:
        print(response.text)

if __name__ == "__main__":
    test_filter_nomenclature()
    test_filter_osv()
