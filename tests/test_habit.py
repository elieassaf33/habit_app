from datetime import datetime
from habit import Habit


def test_habit_creation():
    h = Habit(
        name="Drink Water",
        periodicity="daily",
        id=1,
        created_at=datetime.now(),
        completions=[]
    )

    assert h.name == "Drink Water"
    assert h.periodicity == "daily"
    assert h.get_streak() == 0


def test_prevent_double_completion_daily():
    now = datetime.now()

    h = Habit(
        name="Test",
        periodicity="daily",
        id=1,
        created_at=now,
        completions=[now]
    )

    assert h.complete() is False


def test_prevent_double_completion_weekly():
    now = datetime.now()

    h = Habit(
        name="Test",
        periodicity="weekly",
        id=1,
        created_at=now,
        completions=[now]
    )

    assert h.complete() is False