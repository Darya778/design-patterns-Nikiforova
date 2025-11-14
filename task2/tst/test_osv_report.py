import os
import unittest
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

from src.core.storage_repository import storage_repository
from src.start_service import start_service
from src.logics.osv_service import compute_osv

"""
Тест с генерацией PNG
"""
class TestOSVReport(unittest.TestCase):

    def setUp(self):
        self.repo = storage_repository()
        svc = start_service(self.repo)
        svc.create()

    def test_osv_and_generate_png(self):
        start = date(2025, 1, 1)
        end = date(2025, 1, 31)
        osv = compute_osv(self.repo, start, end, warehouse="Основной склад")

        noms = [r["Номенклатура"]["name"] for r in osv]
        self.assertIn("Мука", noms, "ОСВ должна содержать номенклатуру 'Мука'")

        muka = next(r for r in osv if r["Номенклатура"]["name"] == "Мука")
        self.assertGreaterEqual(muka["Приход"], 0, "Приход по 'Мука' должен быть неотрицательным")

        df = pd.DataFrame([
            {
                "Номенклатура": r["Номенклатура"].get("name", ""),
                "Ед. изм.": r["Единица"].get("name", "") if isinstance(r["Единица"], dict) else r["Единица"],
                "Нач. остаток": r["Начальный остаток"],
                "Приход": r["Приход"],
                "Расход": r["Расход"],
                "Кон. остаток": r["Конечный остаток"]
            }
            for r in osv
        ])

        out_dir = os.path.abspath("data_out")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "osv_report.png")

        fig, ax = plt.subplots(figsize=(9, 1 + 0.5 * len(df)))
        ax.axis('off')

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            loc='center',
            cellLoc='center'
        )

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.4)

        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#4a90e2')
            else:
                cell.set_facecolor('#f9f9f9')

        plt.title(
            f"ОСВ с {start.isoformat()} по {end.isoformat()}, Склад: Основной склад",
            fontsize=12,
            fontweight='bold',
            pad=14
        )

        plt.savefig(out_path, bbox_inches='tight', dpi=200)
        plt.close(fig)

        self.assertTrue(os.path.exists(out_path), f"Файл отчёта {out_path} должен быть создан")


if __name__ == "__main__":
    unittest.main()
