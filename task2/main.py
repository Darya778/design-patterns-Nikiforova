import connexion
from flask import request
from src.models.settings_model import SettingsModel, ResponseFormat
from src.core.factory_entities import FactoryEntities

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
Пример: /api/data?format=markdown
"""
@app.route("/api/data", methods=["GET"])
def get_data():
    # Пример данных
    data = [
        {"id": 1, "name": "Milk"},
        {"id": 2, "name": "Sugar"}
    ]

    fmt = request.args.get("format", "json").upper()
    response_format = ResponseFormat[fmt] if fmt in ResponseFormat.__members__ else ResponseFormat.JSON
    settings = SettingsModel(response_format=response_format)

    factory = FactoryEntities(settings)
    return factory.create_default(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
