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
    return requested.lower() in tx_warehouse.lower()

"""
Формирует оборотно-сальдовую ведомость
"""
def compute_osv(repo, start_date: date, end_date: date, warehouse: str = None):
    txs = repo.transactions
    noms = [n.name for n in repo.nomenclatures]

    result = []
    for n in noms:
        filt = [t for t in txs if t.nomenclature == n and warehouse_match(t.warehouse, warehouse)]
        opening = sum(t.quantity for t in filt if t.date < start_date)
        incoming = sum(t.quantity for t in filt if start_date <= t.date <= end_date and t.quantity > 0)
        outgoing = -sum(t.quantity for t in filt if start_date <= t.date <= end_date and t.quantity < 0)
        closing = opening + incoming - outgoing
        unit = filt[0].unit if filt else ""
        result.append({
            "Номенклатура": n,
            "Единица": unit,
            "Начальный остаток": opening,
            "Приход": incoming,
            "Расход": outgoing,
            "Конечный остаток": closing
        })
    return result
