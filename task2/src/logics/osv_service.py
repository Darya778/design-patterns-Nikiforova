from datetime import date
from src.core.filter_utils import filter_objects
from src.models.filter_dto import FilterDTO
from typing import List


class OSVCalculator:
    def __init__(self, repo):
        """
        repo: объект репозитория с атрибутами:
            - transactions
            - nomenclatures
            - warehouses
        """
        self.repo = repo

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

    def compute_osv(self, start_date, end_date, warehouse: str = None):
        """
        Формирует оборотно-сальдовую ведомость
        """
        txs = self.repo.transactions
        noms = self.repo.nomenclatures

        result = []
        for n in noms:
            filt = [t for t in txs if t.nomenclature == n and self.warehouse_match(t.warehouse, warehouse)]

            if not filt:
                wh_obj = next((w for w in self.repo.warehouses if self.warehouse_match(w, warehouse)), None)
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
                t.unit.to_base(t.quantity) for t in filt if start_date <= t.date <= end_date and t.quantity > 0)
            outgoing = -sum(
                t.unit.to_base(t.quantity) for t in filt if start_date <= t.date <= end_date and t.quantity < 0)
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


"""Прототип сервиса для генерации ОСВ"""
class OSVPrototype:
    def __init__(self, storage):
        self.storage = storage

    def generate_osv(self, model_type: str, filters: List[FilterDTO] = None):
        """Генерирует упрощенную ОСВ для указанного типа модели"""
        objects = getattr(self.storage, model_type + "s", [])
        if filters:
            objects = filter_objects(objects, filters)
        osv_list = []
        for obj in objects:
            osv_list.append({
                "name": getattr(obj, "name", ""),
                "code": getattr(obj, "code", ""),
                "balance": getattr(obj, "balance", 0)
            })
        return osv_list
