"""
Unit tests for Habit creation and completion-prevention logic.

Covers:
- Habit initialization
- Daily and weekly double-completion prevention
"""

from datetime import datetime
from habit import Habit


def test_habit_creation():
    """A newly created habit should have correct attributes and zero streak."""
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
    """Daily habits cannot be completed twice on the same day."""
    now = datetime.now()

    h = Habit(
        name="Test",
        periodicity="daily",
        id=1,
        created_at=now,
        completions=[now]  # already completed today
    )

    assert h.complete() is False


def test_prevent_double_completion_weekly():
    """Weekly habits cannot be completed twice in the same ISO week."""
    now = datetime.now()

    h = Habit(
        name="Test",
        periodicity="weekly",
        id=1,
        created_at=now,
        completions=[now]  # already completed this week
    )

    assert h.complete() is False
