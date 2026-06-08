"""
Unit tests for Habit tracking and analytics functionality.

Covers:
- Daily and weekly streak logic
- Record streak logic (longest historical streak)
- Analytics functions (list_all, list_by_periodicity, longest streaks)
"""

from datetime import datetime, timedelta
from habit import Habit
from analytics import (
    list_all,
    list_by_periodicity,
    longest_streak_all,
    longest_streak_for
)


def make_habit(name, periodicity, streak):
    """
    Create a Habit with a given number of consecutive completions.

    Args:
        name (str): Habit name.
        periodicity (str): "daily" or "weekly".
        streak (int): Number of consecutive completions.

    Returns:
        Habit: A habit instance with generated completion timestamps.
    """
    now = datetime.now()
    completions = []

    for i in range(streak):
        if periodicity == "daily":
            completions.append(now - timedelta(days=i))
        else:  # weekly
            completions.append(now - timedelta(weeks=i))

    return Habit(1, name, periodicity, now, completions)


def test_list_all():
    """list_all should return the same list of habits unchanged."""
    habits = [make_habit("A", "daily", 1)]
    assert list_all(habits) == habits


def test_list_by_periodicity():
    """list_by_periodicity should filter habits by daily/weekly."""
    habits = [
        make_habit("A", "daily", 1),
        make_habit("B", "weekly", 1),
    ]
    daily = list_by_periodicity(habits, "daily")
    assert len(daily) == 1
    assert daily[0].name == "A"


def test_longest_streak_all():
    """longest_streak_all should return the habit with the highest record streak."""
    habits = [
        make_habit("A", "daily", 1),
        make_habit("B", "daily", 5),
    ]
    longest = longest_streak_all(habits)
    assert longest.name == "B"
    assert longest.get_record_streak() == 5


def test_longest_streak_for():
    """longest_streak_for should return the habit with the highest record streak for a given name."""
    habits = [
        make_habit("A", "daily", 3),
        make_habit("B", "weekly", 2),
    ]
    h = longest_streak_for(habits, "A")
    assert h.name == "A"
    assert h.get_record_streak() == 3



def test_record_streak_daily():
    """Record streak should detect the longest daily streak even with gaps."""
    h = Habit(1, "Daily Test", "daily", datetime.now(), [])
    base = datetime.now()

    # 5‑day streak
    for i in range(5):
        h.completions.append(base - timedelta(days=i))

    # gap
    h.completions.append(base - timedelta(days=10))

    # smaller streak
    h.completions.append(base - timedelta(days=20))
    h.completions.append(base - timedelta(days=21))

    assert h.get_record_streak() == 5


def test_record_streak_weekly():
    """Record streak should detect the longest weekly streak even with gaps."""
    h = Habit(1, "Weekly Test", "weekly", datetime.now(), [])
    base = datetime.now()

    # 3‑week streak
    for i in range(3):
        h.completions.append(base - timedelta(weeks=i))

    # gap
    h.completions.append(base - timedelta(weeks=6))

    # smaller streak
    h.completions.append(base - timedelta(weeks=10))
    h.completions.append(base - timedelta(weeks=11))

    assert h.get_record_streak() == 3


def test_record_streak_unsorted_input():
    """Record streak should work even if completion timestamps are unsorted."""
    import random

    h = Habit(1, "Shuffle Test", "daily", datetime.now(), [])
    base = datetime.now()

    # 4‑day streak
    streak_days = [base - timedelta(days=i) for i in range(4)]

    # randomize order
    random.shuffle(streak_days)

    h.completions.extend(streak_days)

    assert h.get_record_streak() == 4

