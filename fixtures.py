# fixtures.py
"""
Provides predefined habits and example completion data for the Habit Tracking App.

This module is used during the development phase to populate the database
with:
    - 5 predefined habits (at least one daily and one weekly)
    - 4 weeks of example completion timestamps for each habit

The data is inserted only if the database is empty, preventing duplicates.
"""

from datetime import datetime, timedelta
from habit import Habit
from storage import Storage
from manager import HabitManager


def load_fixtures(storage: Storage, manager: HabitManager) -> None:
    """
    Load predefined habits and 4 weeks of example completion data.

    This function checks whether the database already contains habits.
    If it is empty, it inserts:
        - 5 predefined habits
        - 4 weeks of completion timestamps for each habit

    Args:
        storage (Storage): The SQLite storage backend.
        manager (HabitManager): The habit manager instance.
    """
    if manager.habits:
        # Database already has data; do not insert duplicates
        return

    # ---------------------------------------------------------
    # 1. Predefined habits
    # ---------------------------------------------------------
    predefined = [
        ("Drink Water", "daily"),
        ("Workout", "daily"),
        ("Read a Book", "daily"),
        ("Clean Apartment", "weekly"),
        ("Grocery Shopping", "weekly"),
    ]

    now = datetime.now()
    habits = []

    for name, periodicity in predefined:
        # Generate completion timestamps first
        completions = []
        if periodicity == "daily":
            # 28 daily completions (4 weeks)
            for i in range(28):
                timestamp = now - timedelta(days=i)
                completions.append(timestamp)
        elif periodicity == "weekly":
            # 4 weekly completions (one per week)
            for i in range(4):
                timestamp = now - timedelta(weeks=i)
                completions.append(timestamp)

        # Set created_at to the oldest completion (first in sequence)
        created_at = completions[-1]

        # Create habit with aligned created_at
        habit_id = storage.insert_habit(name, periodicity, created_at)
        habit = Habit(name=name, periodicity=periodicity, id=habit_id, created_at=created_at)
        habits.append(habit)

        # Insert completions into storage
        for timestamp in completions:
            storage.insert_completion(habit.id, timestamp)
        habit.completions = completions

    # Reload habits in manager to pick up the newly created data
    manager.habits = manager.load_habits()
