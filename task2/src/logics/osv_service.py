from datetime import date

"""
Сравнение склада с фильтром по подстроке (регистронезависимое)
Если склад не задан - всегда True
"""
def warehouse_match(tx_warehouse, requested):
    if not requested:
        return True
    if not tx_warehouse:
        return False
    requested = requested.lower()
    return (
        requested in tx_warehouse.name.lower()
        or requested == getattr(tx_warehouse, "code", "").lower()
    )


"""
Формирует оборотно-сальдовую ведомость
"""
def compute_osv(repo, start_date, end_date, warehouse: str = None):
    txs = repo.transactions
    noms = repo.nomenclatures

    result = []
    for n in noms:
        filt = [t for t in txs if t.nomenclature == n and warehouse_match(t.warehouse, warehouse)]
        if not filt:
            wh_obj = next((w for w in repo.warehouses if warehouse_match(w, warehouse)), None)
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
        incoming = sum(t.unit.to_base(t.quantity) for t in filt if start_date <= t.date <= end_date and t.quantity > 0)
        outgoing = -sum(t.unit.to_base(t.quantity) for t in filt if start_date <= t.date <= end_date and t.quantity < 0)
        closing = opening + incoming - outgoing

        first_unit = filt[0].unit
        base_unit = first_unit.base if first_unit.base else first_unit
        unit_name = base_unit.name

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
