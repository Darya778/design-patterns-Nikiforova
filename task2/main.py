import connexion
from flask import request, Response

from src.core.storage_repository import storage_repository
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.logics.factory_entities import factory_entities


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

    if entity_type == "nomenclature":
        data = [n.to_dict() for n in repo.nomenclatures]
    elif entity_type == "unit":
        data = [u.to_dict() for u in repo.units]
    elif entity_type == "group":
        data = [g.to_dict() for g in repo.groups]
    elif entity_type == "receipt":
        data = [r.to_dict() for r in repo.receipts]
    else:
        return Response(f"Unknown type: {entity_type}", status=400)

    response = factory.create_default(data)

    mime = {
        "csv": "text/csv",
        "json": "application/json",
        "markdown": "text/markdown",
        "xml": "application/xml"
    }.get(fmt, "text/plain")

    return Response(response, status=200, mimetype=mime)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
