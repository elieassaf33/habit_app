from datetime import datetime, timedelta
from habit import Habit

def test_daily_streak():
    now = datetime.now()
    completions = [
        now,
        now - timedelta(days=1),
        now - timedelta(days=2),
    ]
    h = Habit(1, "Daily", "daily", now, completions)

    assert h.get_streak() == 3

def test_daily_streak_break():
    now = datetime.now()
    completions = [
        now,
        now - timedelta(days=1),
        now - timedelta(days=3),  # gap → streak breaks
    ]
    h = Habit(1, "Daily", "daily", now, completions)

    assert h.get_streak() == 2

def test_weekly_streak():
    now = datetime.now()
    completions = [
        now,
        now - timedelta(weeks=1),
        now - timedelta(weeks=2),
    ]
    h = Habit(1, "Weekly", "weekly", now, completions)

    assert h.get_streak() == 3

def test_weekly_streak_break():
    now = datetime.now()
    completions = [
        now,
        now - timedelta(weeks=1),
        now - timedelta(weeks=3),  # gap → streak breaks
    ]
    h = Habit(1, "Weekly", "weekly", now, completions)

    assert h.get_streak() == 2
