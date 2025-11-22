"""
Назначение: хранилище данных для моделей проекта
"""
import os
import json
from datetime import date
from dataclasses import asdict
from typing import List

from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.receipt_model import receipt_model
from src.models.warehouse_model import warehouse_model
from src.models.transaction_model import transaction_model
from src.models.turnover_snapshot_model import turnover_snapshot_model


class storage_repository:
    """
    Репозиторий для хранения всех моделей приложения
    """

    def __init__(self):
        self.nomenclatures = []
        self.units = []
        self.groups = []
        self.receipts = []
        self.warehouses = []
        self.transactions = []

        self.file_path = os.path.join("task2", "data_out", "repository.json")
        self.snapshot_file = os.path.join("task2", "data_out", "turnover_snapshot.json")

        self.data = {
            "nomenclature": self.nomenclatures,
            "unit": self.units,
            "group": self.groups,
            "receipt": self.receipts,
            "warehouse": self.warehouses,
            "transaction": self.transactions
        }

    def add_nomenclature(self, item): self.nomenclatures.append(item)
    def add_unit(self, item): self.units.append(item)
    def add_group(self, item): self.groups.append(item)
    def add_receipt(self, item): self.receipts.append(item)
    def add_warehouse(self, item): self.warehouses.append(item)
    def add_transaction(self, item): self.transactions.append(item)

    def get_warehouse_by_id(self, warehouse_id):
        return next((w for w in self.warehouses if getattr(w, "id", None) == warehouse_id), None)

    def get_nomenclature_by_id(self, item_id):
        return next((n for n in self.nomenclatures if getattr(n, "id", None) == item_id), None)

    def get_unit_by_id(self, unit_id):
        return next((u for u in self.units if getattr(u, "id", None) == unit_id), None)

    def save_all(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        full = {name: [getattr(i, "to_dict", lambda: i.__dict__)() for i in items] for name, items in self.data.items()}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(full, f, ensure_ascii=False, indent=2)

    @staticmethod
    def restore_ref(mapping, container, key):
        ref = container.get(key)
        if isinstance(ref, dict):
            return mapping.get(ref.get("id"))
        return None

    def load_all(self):
        if not os.path.exists(self.file_path):
            return False

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for arr in self.data.values():
            arr.clear()

        id_to_unit = {}

        for u in data.get("unit", []):
            base = None
            if u.get("base"):
                base = unit_model(
                    name=u["base"]["name"],
                    factor=u["base"]["factor"],
                    base=None
                )
                base.id = u["base"].get("id")

            unit = unit_model(
                name=u["name"],
                factor=u["factor"],
                base=base
            )
            unit.id = u.get("id")
            id_to_unit[unit.id] = unit
            self.add_unit(unit)

        id_to_group = {}
        for g in data.get("group", []):
            group = group_model(g["name"])
            group.id = g.get("id")
            id_to_group[group.id] = group
            self.add_group(group)

        id_to_wh = {}
        for w in data.get("warehouse", []):
            wh = warehouse_model(w["name"])
            wh.id = w.get("id")
            wh.code = w.get("code")
            id_to_wh[wh.id] = wh
            self.add_warehouse(wh)

        id_to_nom = {}
        for n in data.get("nomenclature", []):
            grp = id_to_group.get(n["group"]["id"]) if n.get("group") else None
            unt = id_to_unit.get(n["unit"]["id"]) if n.get("unit") else None

            nom = nomenclature_model(
                name=n["name"],
                full_name=n.get("full_name", ""),
                group=grp,
                unit=unt
            )
            nom.id = n.get("id")
            id_to_nom[nom.id] = nom
            self.add_nomenclature(nom)

        for t in data.get("transaction", []):
            nom = self.restore_ref(id_to_nom, t, "nomenclature")
            wh = self.restore_ref(id_to_wh, t, "warehouse")
            unt = self.restore_ref(id_to_unit, t, "unit")

            d = None
            if t.get("date"):
                d = date.fromisoformat(t["date"])

            tr = transaction_model(
                number=t.get("number", f"NO_CODE_{t.get('id', '')}"),
                nomenclature=nom,
                warehouse=wh,
                quantity=t.get("quantity", 0),
                unit=unt,
                date_=d
            )
            tr.id = t.get("id")
            self.add_transaction(tr)

        return True

    def save_turnovers_snapshot(self, block_date: date, data: List[turnover_snapshot_model]):
        """
        Сохраняет snapshot в JSON — сериализуем поля вручную,
        так как date не сериализуется json.dump.
        """
        os.makedirs(os.path.dirname(self.snapshot_file), exist_ok=True)

        payload = {
            "block_date": block_date.isoformat(),
            "data": [
                {
                    "warehouse_id": s.warehouse_id,
                    "item_id": s.item_id,
                    "unit_id": s.unit_id,
                    "closing": s.closing,
                    "snapshot_date": s.snapshot_date.isoformat()
                }
                for s in data
            ]
        }

        with open(self.snapshot_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load_turnovers_snapshot(self, block_date: date) -> List[turnover_snapshot_model] | None:
        """
        Загружает snapshot из файла и десериализует в turnover_snapshot_model.
        Возвращает None если файл отсутствует или дата не совпадает.
        """
        if not os.path.exists(self.snapshot_file):
            return None

        with open(self.snapshot_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if payload.get("block_date") != block_date.isoformat():
            return None

        raw = payload.get("data", [])
        result: List[turnover_snapshot_model] = []
        for s in raw:
            snapshot_date = date.fromisoformat(s["snapshot_date"]) if s.get("snapshot_date") else block_date
            result.append(turnover_snapshot_model(
                warehouse_id=s.get("warehouse_id"),
                item_id=s.get("item_id"),
                unit_id=s.get("unit_id"),
                closing=s.get("closing", 0.0),
                snapshot_date=snapshot_date
            ))
        return result
