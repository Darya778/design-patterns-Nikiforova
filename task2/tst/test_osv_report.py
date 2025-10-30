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

        noms = [r["Номенклатура"] for r in osv]
        self.assertIn("Мука", noms)
        muka = next(r for r in osv if r["Номенклатура"] == "Мука")
        self.assertGreaterEqual(muka["Приход"], 0)

        out_dir = os.path.abspath("data_out")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "osv_report.png")

        df = pd.DataFrame(osv)
        fig, ax = plt.subplots(figsize=(8, 1 + 0.5 * len(df)))
        ax.axis('off')
        tbl = ax.table(cellText=df[["Номенклатура", "Единица", "Начальный остаток",
                                   "Приход", "Расход", "Конечный остаток"]].values,
                       colLabels=["Номенклатура", "Ед.", "Начальный остаток", "Приход", "Расход", "Конечный остаток"],
                       loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1, 1.2)
        plt.title(f'ОСВ с {start.isoformat()} по {end.isoformat()}, Склад: Основной склад', pad=12)
        plt.savefig(out_path, bbox_inches='tight', dpi=150)
        plt.close(fig)

        self.assertTrue(os.path.exists(out_path), f"Ожидается файл отчёта {out_path}")


if __name__ == "__main__":
    unittest.main()
