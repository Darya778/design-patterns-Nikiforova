from src.core.abstract_response import abstract_response

"""
Формирование ответа в формате Markdown-таблицы
"""
class response_md(abstract_response):
    def create_response(self, data: list[dict]) -> str:
        if not data:
            return "Нет данных"

        md_parts = []

        for recipe in data:
            name = recipe.get("name", "Без названия")
            group = recipe.get("group", "")
            portions = recipe.get("portions", 1)
            author = recipe.get("author", "Неизвестен")

            # Заголовок и базовая информация
            md_parts.append(f"# {name}\n")
            md_parts.append(f"**Категория:** {group}\n")
            md_parts.append(f"**Порций:** `{portions}`\n")
            md_parts.append(f"**Автор:** {author}\n")

            # Таблица ингредиентов
            ingredients = recipe.get("ingredients", [])
            units = recipe.get("unit", "гр")

            if ingredients:
                md_parts.append("\n| Ингредиенты | Кол-во |\n|-------------|---------|")
                for ing in ingredients:
                    if isinstance(ing, dict):
                        ing_name = ing.get("name", "—")
                        qty = ing.get("amount", f"1 {units}")
                    else:
                        ing_name = str(ing)
                        qty = f"—"
                    md_parts.append(f"| {ing_name} | {qty} |")

            # Пошаговое приготовление (если есть)
            steps = recipe.get("steps") or recipe.get("instructions")
            if steps:
                md_parts.append("\n## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ\n")
                for i, step in enumerate(steps, 1):
                    md_parts.append(f"{i}. {step}")
            else:
                md_parts.append("\n_Шаги приготовления не указаны._")

            md_parts.append("\n---\n")

        return "\n".join(md_parts)
