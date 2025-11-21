"""
Назначение: хранилище данных для моделей проекта
"""

import os
import json
from datetime import date

from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.receipt_model import receipt_model
from src.models.warehouse_model import warehouse_model
from src.models.transaction_model import transaction_model


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

        self.data = {
            "nomenclature": self.nomenclatures,
            "unit": self.units,
            "group": self.groups,
            "receipt": self.receipts,
            "warehouse": self.warehouses,
            "transaction": self.transactions
        }

        self.snapshot_file = os.path.join("task2", "data_out", "turnover_snapshot.json")

    def add_nomenclature(self, item): self.nomenclatures.append(item)
    def add_unit(self, item): self.units.append(item)
    def add_group(self, item): self.groups.append(item)
    def add_receipt(self, item): self.receipts.append(item)
    def add_warehouse(self, item): self.warehouses.append(item)
    def add_transaction(self, item): self.transactions.append(item)

    def save_all(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        full = {name: [i.to_dict() for i in items] for name, items in self.data.items()}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(full, f, ensure_ascii=False, indent=2)
        print(f"[OK] Repository saved to {self.file_path}")

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

    def save_turnovers_snapshot(self, block_date, data):
        os.makedirs(os.path.dirname(self.snapshot_file), exist_ok=True)
        payload = {
            "block_date": block_date.isoformat(),
            "data": data
        }
        with open(self.snapshot_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load_turnovers_snapshot(self, block_date):
        """Загрузить snapshot, если он соответствует block_period"""
        if not os.path.exists(self.snapshot_file):
            return None

        with open(self.snapshot_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if payload.get("block_date") != block_date.isoformat():
            return None

        return payload.get("data", [])
