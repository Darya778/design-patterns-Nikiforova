"""
OSV service — расчёт ОСВ и управление snapshot'ами.
Использует доменные модели и шаблон "Прототип" (OSVPrototype).
"""
from datetime import date, timedelta
from typing import List, Optional

from src.settings_manager import settings_manager
from src.core.filter_utils import FilterUtils
from src.models.balance_model import balance_model
from src.models.turnover_snapshot_model import turnover_snapshot_model
from src.models.osv_row_model import osv_row_model


class OSVCalculator:
    """
    Калькулятор ОСВ, оперирующий доменными моделями.
    """

    def __init__(self, repo):
        self.repo = repo
        self.settings_manager = settings_manager()
        self.prototype = OSVPrototype(repo)

    def compute_osv(self, start_date: date, end_date: date, warehouse: Optional[str] = None, filters=None) -> List[osv_row_model]:
        """
        Возвращает список osv_row_model за период.
        """
        proto = self.prototype.clone()
        return proto.generate(start_date, end_date, warehouse, filters)

    def compute_turnovers_until_block(self, block_period: date) -> List[turnover_snapshot_model]:
        """
        Рассчитывает агрегированные обороты до block_period с использованием прототипа.
        Прототип гарантирует ЕДИНУЮ логику расчёта ОСВ по модели osv_row_model.
        """
        proto = self.prototype.clone()
        rows = proto.generate(date(1900, 1, 1), block_period)

        snapshot_list: List[turnover_snapshot_model] = []

        for r in rows:
            snapshot_list.append(
                turnover_snapshot_model(
                    warehouse_id=r.warehouse.id if r.warehouse else None,
                    item_id=r.item.id,
                    unit_id=r.unit.id if r.unit else None,
                    closing=r.closing,
                    snapshot_date=block_period
                )
            )

        self.repo.save_turnovers_snapshot(block_period, snapshot_list)

        return snapshot_list

    def compute_balances_at(self, target_date: date) -> List[balance_model]:
        """
        Возвращает остатки на target_date с учётом сохранённого snapshot до даты блокировки.
        Всегда возвращает список balance_model.
        """
        block_date = self.settings_manager.get_block_period()

        if not block_date:
            rows = self.prototype.generate(date(1900, 1, 1), target_date)
            return [
                balance_model(
                    warehouse=r.warehouse,
                    item=r.item,
                    unit=r.unit,
                    balance=r.closing
                ) for r in rows
            ]

        snapshot = self.repo.load_turnovers_snapshot(block_date)
        if snapshot is None:
            snapshot = self.compute_turnovers_until_block(block_date)

        if target_date <= block_date:
            balances = []
            for s in snapshot:
                wh = self.repo.get_warehouse_by_id(s.warehouse_id) if s.warehouse_id is not None else None
                item = self.repo.get_nomenclature_by_id(s.item_id)
                unit = self.repo.get_unit_by_id(s.unit_id) if s.unit_id is not None else None
                balances.append(balance_model(warehouse=wh, item=item, unit=unit, balance=s.closing))
            return balances

        balances_map = {
            (s.warehouse_id, s.item_id, s.unit_id): s.closing
            for s in snapshot
        }

        after_start = block_date + timedelta(days=1)
        txs = [t for t in self.repo.transactions if t.date and after_start <= t.date <= target_date]

        for t in txs:
            key = (t.warehouse.id if t.warehouse else None, t.nomenclature.id, t.unit.id if t.unit else None)
            qty = t.unit.to_base(t.quantity) if getattr(t, "unit", None) and hasattr(t.unit, "to_base") else t.quantity
            balances_map[key] = balances_map.get(key, 0.0) + qty

        result = []
        for (wh_id, item_id, unit_id), bal in balances_map.items():
            wh = self.repo.get_warehouse_by_id(wh_id) if wh_id is not None else None
            item = self.repo.get_nomenclature_by_id(item_id)
            unit = self.repo.get_unit_by_id(unit_id) if unit_id is not None else None
            result.append(balance_model(warehouse=wh, item=item, unit=unit, balance=bal))

        return result


"""Прототип сервиса для генерации ОСВ"""
class OSVPrototype:
    """
    Прототип, формирующий ОСВ как список osv_row_model
    """

    def __init__(self, storage):
        self.storage = storage

    def clone(self):
        """
        Возвращает новый экземпляр прототипа.
        """
        return OSVPrototype(self.storage)

    def generate(self, start_date: date, end_date: date, warehouse: Optional[str] = None, filters=None) -> List[osv_row_model]:
        """
        Собирает ОСВ (в виде domain моделей) за указанный период.
        Поддерживает фильтры: фильтры применяются к табличному представлению,
        затем строки восстанавливаются обратно в модели.
        """
        result: List[osv_row_model] = []

        noms = self.storage.nomenclatures
        txs = self.storage.transactions

        for n in noms:
            relevant = [
                t for t in txs
                if t.nomenclature == n and self._warehouse_match(t.warehouse, warehouse)
            ]

            if not relevant:
                wh_obj = next(
                    (w for w in self.storage.warehouses if self._warehouse_match(w, warehouse)),
                    None
                )
                result.append(osv_row_model(
                    warehouse=wh_obj,
                    item=n,
                    unit=n.unit,
                    opening=0.0,
                    incoming=0.0,
                    outgoing=0.0
                ))
                continue

            opening = sum(t.unit.to_base(t.quantity) for t in relevant if t.date < start_date)
            incoming = sum(t.unit.to_base(t.quantity) for t in relevant if start_date <= t.date <= end_date and t.quantity > 0)
            outgoing = -sum(t.unit.to_base(t.quantity) for t in relevant if start_date <= t.date <= end_date and t.quantity < 0)

            base_unit = relevant[0].unit.base if relevant[0].unit and getattr(relevant[0].unit, "base", None) else (relevant[0].unit if getattr(relevant[0], "unit", None) else None)

            result.append(osv_row_model(
                warehouse=relevant[0].warehouse,
                item=n,
                unit=base_unit,
                opening=opening,
                incoming=incoming,
                outgoing=outgoing
            ))

        if filters:
            raw = [
                {
                    "Склад": r.warehouse.to_dict() if r.warehouse else {"name": "Все склады"},
                    "Номенклатура": r.item.to_dict(),
                    "Единица": r.unit.to_dict() if r.unit else {},
                    "Начальный остаток": r.opening,
                    "Приход": r.incoming,
                    "Расход": r.outgoing,
                    "Конечный остаток": r.closing
                }
                for r in result
            ]

            raw_filtered = FilterUtils.apply(raw, filters)

            new_result: List[osv_row_model] = []
            for r in raw_filtered:
                wh_id = r.get("Склад", {}).get("id")
                nom_id = r["Номенклатура"]["id"]
                unit_id = r.get("Единица", {}).get("id")

                wh = self.storage.get_warehouse_by_id(wh_id) if wh_id is not None else None
                nom = self.storage.get_nomenclature_by_id(nom_id)
                unit = self.storage.get_unit_by_id(unit_id) if unit_id is not None else None

                new_result.append(osv_row_model(
                    warehouse=wh,
                    item=nom,
                    unit=unit,
                    opening=r.get("Начальный остаток", 0.0),
                    incoming=r.get("Приход", 0.0),
                    outgoing=r.get("Расход", 0.0)
                ))

            result = new_result

        return result

    @staticmethod
    def _warehouse_match(tx_wh, wanted):
        if not wanted:
            return True
        if tx_wh is None:
            return False
        wanted = wanted.lower()
        return wanted in tx_wh.name.lower() or wanted == getattr(tx_wh, "code", "").lower()
