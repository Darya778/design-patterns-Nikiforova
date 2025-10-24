import connexion
from flask import request, Response, jsonify
from datetime import datetime
import json

from src.core.storage_repository import storage_repository
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.logics.factory_entities import factory_entities
from src.logics.convert_factory import convert_factory


app = connexion.FlaskApp(__name__)

"""
Маршрут проверки доступности API
Используется для теста работоспособности сервиса
"""
@app.route("/api/accessibility", methods=["GET"])
def accessibility():
    return "SUCCESS"


"""
Маршрут для получения данных в выбранном формате
http://127.0.0.1:8080/api/data?type=receipt&format=xml
"""
@app.route("/api/data", methods=["GET"])
def get_data():
    entity_type = request.args.get("type", "nomenclature").lower()
    fmt = request.args.get("format", "json").lower()

    repo = storage_repository()
    service = start_service(repo)
    service.create()

    settings = settings_manager()
    settings.default()
    settings.response_format = fmt

    factory = factory_entities(settings)

    if entity_type not in repo.data:
        raise ValueError(f"Неизвестный тип данных: {entity_type}")

    data = [item.to_dict() for item in repo.data[entity_type]]
    response = factory.create_default(data)

    mime = {
        "csv": "text/csv",
        "json": "application/json",
        "markdown": "text/markdown",
        "xml": "application/xml"
    }.get(fmt, "text/plain")

    return Response(response, status=200, mimetype=mime)


"""
Возвращает справочник в JSON, используя convert_factory
Пример: /api/reference/nomenclature
"""
@app.route("/api/reference/<entity_type>", methods=["GET"])
def get_reference(entity_type: str):
    repo = storage_repository()
    service = start_service(repo)
    service.create()

    if entity_type not in repo.data:
        return jsonify({"error": f"Unknown entity type: {entity_type}"}), 404

    converter = convert_factory()
    result = converter.convert_collection(repo.data[entity_type])

    return Response(json.dumps(result, ensure_ascii=False), mimetype="application/json", status=200)


"""
Возвращает список рецептов (в JSON)
"""
@app.route("/api/receipts", methods=["GET"])
def get_receipts():
    repo = storage_repository()
    service = start_service(repo)
    service.create()

    if "receipt" not in repo.data:
        return jsonify({"error": "Receipt data not found"}), 404

    converter = convert_factory()
    receipts = converter.convert_collection(repo.data["receipt"])

    return Response(json.dumps(receipts, ensure_ascii=False), mimetype="application/json", status=200)


"""
Возвращает конкретный рецепт по коду
Пример: /api/receipt?code=RC100
"""
@app.route("/api/receipt", methods=["GET"])
def get_receipt():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Parameter 'code' is required"}), 400

    repo = storage_repository()
    service = start_service(repo)
    service.create()

    if "receipt" not in repo.data:
        return jsonify({"error": "Receipt data not found"}), 404

    receipt = next((r for r in repo.data["receipt"] if getattr(r, "code", None) == code), None)
    if not receipt:
        return jsonify({"error": f"Receipt with code '{code}' not found"}), 404

    converter = convert_factory()
    result = converter.convert(receipt)

    return Response(json.dumps(result, ensure_ascii=False), mimetype="application/json", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
