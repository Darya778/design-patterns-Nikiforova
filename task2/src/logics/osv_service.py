from datetime import date
from src.core.filter_utils import FilterUtils
from src.models.filter_dto import FilterDTO
from src.core.filter_engine import filter_engine
from typing import List
from datetime import datetime, date, timedelta
from src.settings_manager import settings_manager

class OSVCalculator:

    def __init__(self, repo):
        self.repo = repo
        self.prototype = OSVPrototype(repo)
        self.settings_manager = settings_manager()

    def compute_osv(self, start_date, end_date, warehouse=None, filters=None):
        proto = self.prototype.clone()
        return proto.generate(start_date, end_date, warehouse, filters)

    @staticmethod
    def warehouse_match(tx_warehouse, requested):
        """
        Сравнение склада с фильтром по подстроке (регистронезависимое)
        Если склад не задан - всегда True
        """
        if not requested:
            return True
        if not tx_warehouse:
            return False
        requested = requested.lower()
        return (
                requested in tx_warehouse.name.lower()
                or requested == getattr(tx_warehouse, "code", "").lower()
        )

    def _compute_internal(self, start_date, end_date, warehouse):
        """
        Базовая логика формирования ОСВ
        """
        txs = self.repo.transactions
        noms = self.repo.nomenclatures

        result = []

        for n in noms:
            filt = [
                t for t in txs
                if t.nomenclature == n and self.warehouse_match(t.warehouse, warehouse)
            ]

            if not filt:
                wh_obj = next(
                    (w for w in self.repo.warehouses if self.warehouse_match(w, warehouse)),
                    None
                )
                result.append({
                    "Склад": wh_obj.to_dict() if wh_obj else {"name": warehouse or "Все склады"},
                    "Номенклатура": n.to_dict(),
                    "Единица": n.unit.to_dict() if n.unit else {},
                    "Начальный остаток": 0,
                    "Приход": 0,
                    "Расход": 0,
                    "Конечный остаток": 0
                })
                continue

            opening = sum(t.unit.to_base(t.quantity) for t in filt if t.date < start_date)
            incoming = sum(
                t.unit.to_base(t.quantity)
                for t in filt if start_date <= t.date <= end_date and t.quantity > 0
            )
            outgoing = -sum(
                t.unit.to_base(t.quantity)
                for t in filt if start_date <= t.date <= end_date and t.quantity < 0
            )
            closing = opening + incoming - outgoing

            first_unit = filt[0].unit
            base_unit = first_unit.base if first_unit.base else first_unit

            result.append({
                "Склад": filt[0].warehouse.to_dict(),
                "Номенклатура": n.to_dict(),
                "Единица": base_unit.to_dict() if base_unit else {},
                "Начальный остаток": opening,
                "Приход": incoming,
                "Расход": outgoing,
                "Конечный остаток": closing
            })

        return result

    def compute_turnovers_until_block(self, block_period: date):
        start_date = date(1900, 1, 1)
        end_date = block_period

        txs = [t for t in self.repo.transactions if t.date and t.date <= end_date]

        snapshots = {}
        for t in txs:
            key = (
                t.warehouse.id if t.warehouse else None,
                t.nomenclature.id,
                t.unit.id if t.unit else None
            )
            entry = snapshots.setdefault(key, {"opening": 0.0, "incoming": 0.0, "outgoing": 0.0})
            qty = t.unit.to_base(t.quantity) if getattr(t, "unit", None) and hasattr(t.unit, "to_base") else t.quantity
            if t.date < start_date:
                entry["opening"] += qty
            else:
                if qty >= 0:
                    entry["incoming"] += qty
                else:
                    entry["outgoing"] += -qty

        snapshot_list = []
        for (wh_id, item_id, unit_id), vals in snapshots.items():
            snapshot_list.append({
                "warehouse_id": wh_id,
                "item_id": item_id,
                "unit_id": unit_id,
                "opening": vals["opening"],
                "incoming": vals["incoming"],
                "outgoing": vals["outgoing"],
                "closing": vals["opening"] + vals["incoming"] - vals["outgoing"],
                "snapshot_date": end_date.isoformat()
            })

        self.repo.save_turnovers_snapshot(end_date, snapshot_list)

        return snapshot_list

    def compute_balances_at(self, target_date: date):
        block_date = self.settings_manager.get_block_period()

        if not block_date:
            return self.prototype.generate(date(1900, 1, 1), target_date)

        snapshot = self.repo.load_turnovers_snapshot(block_date)
        if snapshot is None:
            snapshot = self.compute_turnovers_until_block(block_date)

        if target_date <= block_date:
            return [
                {
                    "warehouse_id": s["warehouse_id"],
                    "item_id": s["item_id"],
                    "unit_id": s["unit_id"],
                    "balance": s["closing"]
                }
                for s in snapshot
            ]

        balances = {
            (s["warehouse_id"], s["item_id"], s["unit_id"]): s["closing"]
            for s in snapshot
        }

        after_start = block_date + timedelta(days=1)
        txs = [t for t in self.repo.transactions if t.date and after_start <= t.date <= target_date]

        for t in txs:
            key = (t.warehouse.id if t.warehouse else None, t.nomenclature.id, t.unit.id if t.unit else None)
            qty = t.unit.to_base(t.quantity) if getattr(t, "unit", None) and hasattr(t.unit, "to_base") else t.quantity
            balances[key] = balances.get(key, 0.0) + qty

        return [
            {"warehouse_id": wh, "item_id": it, "unit_id": un, "balance": bal}
            for (wh, it, un), bal in balances.items()
        ]


"""Прототип сервиса для генерации ОСВ"""
class OSVPrototype:

    def __init__(self, storage):
        self.storage = storage

    def clone(self):
        """
        Классический метод прототипа.
        Возвращает новый независимый объект с теми же данными.
        """
        return OSVPrototype(self.storage)

    def generate(self, start_date, end_date, warehouse=None, filters=None):

        result = []

        noms = self.storage.nomenclatures
        txs = self.storage.transactions

        for n in noms:
            filt = [
                t for t in txs
                if t.nomenclature == n and self._warehouse_match(t.warehouse, warehouse)
            ]

            if not filt:
                wh_obj = next(
                    (w for w in self.storage.warehouses if self._warehouse_match(w, warehouse)),
                    None
                )
                row = {
                    "Склад": wh_obj.to_dict() if wh_obj else {"name": warehouse or "Все склады"},
                    "Номенклатура": n.to_dict(),
                    "Единица": n.unit.to_dict() if n.unit else {},
                    "Начальный остаток": 0,
                    "Приход": 0,
                    "Расход": 0,
                    "Конечный остаток": 0
                }
            else:
                opening = sum(t.unit.to_base(t.quantity) for t in filt if t.date < start_date)
                incoming = sum(
                    t.unit.to_base(t.quantity)
                    for t in filt if start_date <= t.date <= end_date and t.quantity > 0
                )
                outgoing = -sum(
                    t.unit.to_base(t.quantity)
                    for t in filt if start_date <= t.date <= end_date and t.quantity < 0
                )

                closing = opening + incoming - outgoing
                base_unit = filt[0].unit.base if filt[0].unit.base else filt[0].unit

                row = {
                    "Склад": filt[0].warehouse.to_dict(),
                    "Номенклатура": n.to_dict(),
                    "Единица": base_unit.to_dict(),
                    "Начальный остаток": opening,
                    "Приход": incoming,
                    "Расход": outgoing,
                    "Конечный остаток": closing
                }

            result.append(row)

        if filters:
            result = FilterUtils.apply(result, filters)

        return result

    @staticmethod
    def _warehouse_match(tx_wh, wanted):
        if not wanted:
            return True
        if tx_wh is None:
            return False
        wanted = wanted.lower()
        return wanted in tx_wh.name.lower() or wanted == getattr(tx_wh, "code", "").lower()
