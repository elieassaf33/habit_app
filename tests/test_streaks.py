"""
Unit tests for streak and record-streak logic in the Habit class.

Covers:
- Daily streak calculation
- Weekly streak calculation
- Streak breaking logic
- Record streak detection (daily + weekly)
- Handling of unsorted completion timestamps
"""

from datetime import datetime, timedelta
from habit import Habit



def test_daily_streak():
    """Daily streak should count consecutive days correctly."""
    now = datetime.now()
    completions = [
        now,
        now - timedelta(days=1),
        now - timedelta(days=2),
    ]
    h = Habit(1, "Daily", "daily", now, completions)

    assert h.get_streak() == 3


def test_daily_streak_break():
    """Daily streak should stop when a gap in days appears."""
    now = datetime.now()
    completions = [
        now,
        now - timedelta(days=1),
        now - timedelta(days=3),  # gap → streak breaks
    ]
    h = Habit(1, "Daily", "daily", now, completions)

    assert h.get_streak() == 2


def test_weekly_streak():
    """Weekly streak should count consecutive ISO weeks correctly."""
    now = datetime.now()
    completions = [
        now,
        now - timedelta(weeks=1),
        now - timedelta(weeks=2),
    ]
    h = Habit(1, "Weekly", "weekly", now, completions)

    assert h.get_streak() == 3


def test_weekly_streak_break():
    """Weekly streak should stop when a gap in weeks appears."""
    now = datetime.now()
    completions = [
        now,
        now - timedelta(weeks=1),
        now - timedelta(weeks=3),  # gap → streak breaks
    ]
    h = Habit(1, "Weekly", "weekly", now, completions)

    assert h.get_streak() == 2


def test_record_streak_daily():
    """Record streak should detect the longest daily streak even with gaps."""
    now = datetime.now()
    h = Habit(1, "Daily", "daily", now, [])

    # 5‑day streak
    for i in range(5):
        h.completions.append(now - timedelta(days=i))

    # gap
    h.completions.append(now - timedelta(days=10))

    # smaller streak (2 days)
    h.completions.append(now - timedelta(days=20))
    h.completions.append(now - timedelta(days=21))

    assert h.get_record_streak() == 5


def test_record_streak_weekly():
    """Record streak should detect the longest weekly streak even with gaps."""
    now = datetime.now()
    h = Habit(1, "Weekly", "weekly", now, [])

    # 3‑week streak
    for i in range(3):
        h.completions.append(now - timedelta(weeks=i))

    # gap
    h.completions.append(now - timedelta(weeks=6))

    # smaller streak (2 weeks)
    h.completions.append(now - timedelta(weeks=10))
    h.completions.append(now - timedelta(weeks=11))

    assert h.get_record_streak() == 3


def test_record_streak_unsorted():
    """Record streak should work even if completion timestamps are unsorted."""
    import random
    now = datetime.now()
    h = Habit(1, "Daily", "daily", now, [])

    # 4‑day streak
    streak = [now - timedelta(days=i) for i in range(4)]
    random.shuffle(streak)

    h.completions.extend(streak)

    assert h.get_record_streak() == 4
