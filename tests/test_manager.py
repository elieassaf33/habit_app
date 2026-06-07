from datetime import datetime
from manager import HabitManager
from storage import Storage

def test_create_habit(tmp_path):
    db = tmp_path / "test.db"
    storage = Storage(str(db))
    manager = HabitManager(storage)

    manager.create_habit("Test", "daily")
    assert len(manager.habits) == 1
    assert manager.habits[0].name == "Test"

def test_complete_habit(tmp_path):
    db = tmp_path / "test.db"
    storage = Storage(str(db))
    manager = HabitManager(storage)

    h = manager.create_habit("Test", "daily")
    success = manager.complete_habit(h.id)

    assert success is True
    assert len(h.completions) == 1

def test_prevent_double_completion(tmp_path):
    db = tmp_path / "test.db"
    storage = Storage(str(db))
    manager = HabitManager(storage)

    h = manager.create_habit("Test", "daily")
    manager.complete_habit(h.id)

    # second completion same day → blocked
    success = manager.complete_habit(h.id)
    assert success is False
