from datetime import datetime, timedelta
from habit import Habit
from analytics import (
    list_all,
    list_by_periodicity,
    longest_streak_all,
    longest_streak_for
)


def make_habit(name, periodicity, streak):
    now = datetime.now()
    completions = []

    for i in range(streak):
        if periodicity == "daily":
            completions.append(now - timedelta(days=i))
        else:  # weekly
            completions.append(now - timedelta(weeks=i))

    return Habit(1, name, periodicity, now, completions)


def test_list_all():
    habits = [make_habit("A", "daily", 1)]
    assert list_all(habits) == habits

def test_list_by_periodicity():
    habits = [
        make_habit("A", "daily", 1),
        make_habit("B", "weekly", 1),
    ]
    daily = list_by_periodicity(habits, "daily")
    assert len(daily) == 1
    assert daily[0].name == "A"

def test_longest_streak_all():
    habits = [
        make_habit("A", "daily", 1),
        make_habit("B", "daily", 5),
    ]
    longest = longest_streak_all(habits)
    assert longest.name == "B"

def test_longest_streak_for():
    habits = [
        make_habit("A", "daily", 3),
        make_habit("B", "weekly", 2),
    ]
    h = longest_streak_for(habits, "A")
    assert h.name == "A"
    assert h.get_streak() == 3
