import time, random
from datetime import date, timedelta
from src.core.storage_repository import storage_repository
from src.logics.osv_service import OSVCalculator
from src.models.nomenclature_model import nomenclature_model
from src.models.unit_model import unit_model
from src.models.group_model import group_model
from src.models.warehouse_model import warehouse_model
from datetime import date
from src.settings_manager import settings_manager
settings_manager._instance = None
settings = settings_manager(config_path="benchmarks/settings.json")


def generate_random_transactions(repo, count=1000, start_date=date(2023,1,1), days_span=365):
    items = repo.nomenclatures
    warehouses = repo.warehouses
    units = repo.units
    for i in range(count):
        tdate = start_date + timedelta(days=random.randint(0, days_span))
        item = random.choice(items)
        wh = random.choice(warehouses)
        unit = random.choice(units)
        qty = random.uniform(-50, 100)
        from src.models.transaction_model import transaction_model
        tr = transaction_model(number=f"TX{i}", nomenclature=item, warehouse=wh, quantity=qty, unit=unit, date_=tdate)
        repo.add_transaction(tr)

if __name__ == "__main__":
    repo = storage_repository()
    repo.transactions.clear()

    u = unit_model("шт", 1, None)
    u.id = 1
    repo.add_unit(u)

    g = group_model("Продукты")
    g.id = 1
    repo.add_group(g)

    nom = nomenclature_model("Товар A", "Товар A", g, u)
    nom.id = 1
    repo.add_nomenclature(nom)

    wh = warehouse_model("Склад №1")
    wh.id = 1
    repo.add_warehouse(wh)

    for n in (1000, 5000, 10000):
        repo.transactions.clear()
        generate_random_transactions(repo, count=n)
        osv = OSVCalculator(repo)
        osv.settings_manager.set_block_period(date(2024,1,1))
        t0 = time.time()
        osv.compute_turnovers_until_block(osv.settings_manager.get_block_period())
        snap_t = time.time() - t0

        t0 = time.time()
        osv.compute_balances_at(date(2024,10,1))
        bal_t = time.time() - t0

        print(f"n={n}, snapshot={snap_t:.3f}s, balances={bal_t:.3f}s")
