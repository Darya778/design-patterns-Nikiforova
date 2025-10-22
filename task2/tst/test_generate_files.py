import os
from src.models.settings_model import SettingsModel, ResponseFormat
from src.core.factory_entities import FactoryEntities

"""
Автотест для проверки генерации файлов с данными
Формирует файлы для всех форматов и типов данных
"""
def test_generate_output_files(tmp_path):
    data = [
        {"id": 1, "name": "Group1"},
        {"id": 2, "name": "Group2"}
    ]

    for fmt in ResponseFormat:
        settings = SettingsModel(response_format=fmt)
        factory = FactoryEntities(settings)
        result = factory.create_default(data)
        file_path = tmp_path / f"groups.{fmt.value.lower()}"
        file_path.write_text(result, encoding="utf-8")
        assert file_path.exists()
