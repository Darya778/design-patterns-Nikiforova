import pytest
from datetime import date
from src.core.storage_repository import storage_repository
from src.settings_manager import settings_manager
from src.logics.osv_service import OSVCalculator
from src.models.transaction_model import transaction_model
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model
from src.models.unit_model import unit_model


@pytest.fixture
def repository() -> storage_repository:
    """
    Создаёт изолированный репозиторий с одной номенклатурой,
    одним складом и одной единицей измерения.
    """
    repo = storage_repository()

    unit = unit_model(name="kg", factor=1, base=None)
    unit.id = 1

    item = nomenclature_model(name="Test", full_name="Test Item", group=None, unit=unit)
    item.id = 10

    warehouse = warehouse_model(name="Main Warehouse")
    warehouse.id = 100

    repo.add_unit(unit)
    repo.add_nomenclature(item)
    repo.add_warehouse(warehouse)

    return repo


@pytest.fixture
def settings(tmp_path, monkeypatch) -> settings_manager:
    """
    Создаёт временный settings.json и подменяет путь до него.
    """
    cfg_file = tmp_path / "settings.json"
    cfg_file.write_text("{}", encoding="utf-8")

    sm = settings_manager(file_name=str(cfg_file), config_path=str(cfg_file))
    monkeypatch.setattr(sm, "config_path", str(cfg_file))

    sm.load_settings()
    return sm


def add_transaction(repo, dt, qty):
    """
    Утилита для добавления транзакции в репозиторий.
    """
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


def test_snapshot_created_and_loaded_compute_turnovers_until_block_correct_snapshot(repository, settings):
    """
    Проверяет:
    1. Снимок оборотов создаётся корректно.
    2. Сохраняется в хранилище.
    3. Корректно загружается.
    """
    osv = OSVCalculator(repository)
    osv.settings_manager = settings

    add_transaction(repository, date(2023, 1, 10), 10)
    add_transaction(repository, date(2023, 1, 20), -5)

    block = date(2023, 2, 1)
    settings.set_block_period(block)

    snapshot = osv.compute_turnovers_until_block(block)

    assert len(snapshot) == 1
    assert snapshot[0].closing == 5

    loaded = repository.load_turnovers_snapshot(block)
    assert loaded is not None
    assert snapshot[0].closing == 5


def test_correct_balance_before_block_compute_balances_at_uses_snapshot(repository, settings):
    """
    Проверяет корректность расчёта баланса, если дата запроса < block_period.
    Используется snapshot.
    """
    osv = OSVCalculator(repository)
    osv.settings_manager = settings

    add_transaction(repository, date(2023, 1, 10), 10)
    add_transaction(repository, date(2023, 1, 20), -3)

    block = date(2023, 2, 1)
    settings.set_block_period(block)

    osv.compute_turnovers_until_block(block)

    balances = osv.compute_balances_at(date(2023, 1, 25))

    assert balances[0].balance == 7


def test_correct_balance_after_block_compute_balances_at_adds_post_block_turnovers(repository, settings):
    """
    Проверяет корректность расчёта баланса после block_period —
    snapshot + обороты после block_period.
    """
    osv = OSVCalculator(repository)
    osv.settings_manager = settings

    add_transaction(repository, date(2023, 1, 10), 10)
    add_transaction(repository, date(2023, 1, 20), -2)
    add_transaction(repository, date(2023, 2, 5), 5)

    block = date(2023, 2, 1)
    settings.set_block_period(block)

    osv.compute_turnovers_until_block(block)
    balances = osv.compute_balances_at(date(2023, 2, 10))

    assert balances[0].balance == 13  # (10 – 2) + 5


def test_final_balance_unchanged_when_block_period_changes_compute_balances_stable(repository, settings):
    """
    Главное требование задачи:
    изменение block_period не должно менять итоговый баланс.
    """
    osv = OSVCalculator(repository)
    osv.settings_manager = settings

    add_transaction(repository, date(2023, 1, 1), 10)
    add_transaction(repository, date(2023, 3, 1), -2)
    add_transaction(repository, date(2023, 5, 1), 7)

    final_date = date(2023, 6, 1)

    settings.set_block_period(date(2023, 2, 1))
    osv.compute_turnovers_until_block(date(2023, 2, 1))
    balance1 = osv.compute_balances_at(final_date)[0].balance

    settings.set_block_period(date(2023, 4, 1))
    osv.compute_turnovers_until_block(date(2023, 4, 1))
    balance2 = osv.compute_balances_at(final_date)[0].balance

    assert balance1 == balance2


def test_snapshot_recomputed_when_block_period_changes_new_snapshot_differs(repository, settings):
    """
    Проверяет:
    - при изменении даты блокировки новый snapshot отличается от старого.
    """
    osv = OSVCalculator(repository)
    osv.settings_manager = settings

    add_transaction(repository, date(2023, 1, 10), 10)

    block1 = date(2023, 2, 1)
    settings.set_block_period(block1)
    osv.compute_turnovers_until_block(block1)
    snap1 = repository.load_turnovers_snapshot(block1)[0].closing

    add_transaction(repository, date(2023, 1, 15), 5)

    block2 = date(2023, 3, 1)
    settings.set_block_period(block2)
    osv.compute_turnovers_until_block(block2)
    snap2 = repository.load_turnovers_snapshot(block2)[0].closing

    assert snap1 != snap2
