import pytest
from datetime import date, timedelta
from src.core.storage_repository import storage_repository
from src.settings_manager import settings_manager
from src.logics.osv_service import OSVCalculator
from src.models.transaction_model import transaction_model
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model
from src.models.unit_model import unit_model


@pytest.fixture
def repo():
    """Создаёт пустой репозиторий с 1 номенклатурой, 1 складом и 1 единицей"""
    r = storage_repository()

    u = unit_model(name="kg", factor=1, base=None)
    u.id = 1

    n = nomenclature_model(name="Test Item", full_name="Test", group=None, unit=u)
    n.id = 10

    w = warehouse_model(name="Main Warehouse")
    w.id = 100

    r.add_unit(u)
    r.add_nomenclature(n)
    r.add_warehouse(w)

    return r

@pytest.fixture
def settings(tmp_path, monkeypatch):
    """Изолированный settings.json для тестов"""
    cfg_file = tmp_path / "settings.json"

    cfg_file.write_text("{}", encoding="utf-8")

    s = settings_manager(file_name=str(cfg_file), config_path=str(cfg_file))

    monkeypatch.setattr(s, "config_path", str(cfg_file))

    return s


def add_tx(repo, dt, qty):
    """Удобная функция для добавления транзакции"""
    t = transaction_model(
        number="TX",
        nomenclature=repo.nomenclatures[0],
        warehouse=repo.warehouses[0],
        quantity=qty,
        unit=repo.units[0],
        date_=dt
    )
    t.id = len(repo.transactions) + 1
    repo.add_transaction(t)

def test_snapshot_created_and_loaded(repo, settings):
    osv = OSVCalculator(repo)
    osv.settings_manager = settings

    add_tx(repo, date(2023, 1, 10), 10)
    add_tx(repo, date(2023, 1, 20), -5)

    block = date(2023, 2, 1)
    settings.set_block_period(block)

    snapshot = osv.compute_turnovers_until_block(block)
    assert len(snapshot) == 1
    assert snapshot[0]["closing"] == 5

    loaded = repo.load_turnovers_snapshot(block)
    assert loaded is not None
    assert loaded[0]["closing"] == 5

def test_balances_before_block_period(repo, settings):
    osv = OSVCalculator(repo)
    osv.settings_manager = settings

    add_tx(repo, date(2023, 1, 10), 10)
    add_tx(repo, date(2023, 1, 20), -3)

    block = date(2023, 2, 1)
    settings.set_block_period(block)
    osv.compute_turnovers_until_block(block)

    balances = osv.compute_balances_at(date(2023, 1, 25))
    assert balances[0]["balance"] == 7  # 10 - 3

def test_balances_after_block_period(repo, settings):
    osv = OSVCalculator(repo)
    osv.settings_manager = settings

    add_tx(repo, date(2023, 1, 10), 10)
    add_tx(repo, date(2023, 1, 20), -2)

    add_tx(repo, date(2023, 2, 5), 5)

    block = date(2023, 2, 1)
    settings.set_block_period(block)

    osv.compute_turnovers_until_block(block)

    balances = osv.compute_balances_at(date(2023, 2, 10))

    assert balances[0]["balance"] == 13

def test_final_balance_does_not_change_when_block_period_changes(repo, settings):
    """
    Главное требование задачи:
    изменение block_period не должно менять конечный баланс.
    """
    osv = OSVCalculator(repo)
    osv.settings_manager = settings

    add_tx(repo, date(2023, 1, 1), 10)
    add_tx(repo, date(2023, 3, 1), -2)
    add_tx(repo, date(2023, 5, 1), 7)

    FINAL_DATE = date(2023, 6, 1)

    settings.set_block_period(date(2023, 2, 1))
    osv.compute_turnovers_until_block(date(2023, 2, 1))
    b1 = osv.compute_balances_at(FINAL_DATE)[0]["balance"]

    settings.set_block_period(date(2023, 4, 1))
    osv.compute_turnovers_until_block(date(2023, 4, 1))
    b2 = osv.compute_balances_at(FINAL_DATE)[0]["balance"]

    assert b1 == b2

def test_snapshot_recomputed_after_block_change(repo, settings):
    osv = OSVCalculator(repo)
    osv.settings_manager = settings

    add_tx(repo, date(2023, 1, 10), 10)

    block1 = date(2023, 2, 1)
    settings.set_block_period(block1)
    osv.compute_turnovers_until_block(block1)
    snap1 = repo.load_turnovers_snapshot(block1)[0]["closing"]

    add_tx(repo, date(2023, 1, 15), 5)

    block2 = date(2023, 3, 1)
    settings.set_block_period(block2)
    osv.compute_turnovers_until_block(block2)
    snap2 = repo.load_turnovers_snapshot(block2)[0]["closing"]

    assert snap1 != snap2
