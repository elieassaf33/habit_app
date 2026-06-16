# manager.py
from datetime import datetime
from habit import Habit
from storage import Storage

class HabitManager:
    """
    Coordinates all habit-related operations.
    Acts as the central controller between the UI, storage layer,
    and analytics functions.

    Responsibilities:
        - Load habits and their completions from storage.
        - Create new habits.
        - Record habit completions.
        - Provide access to the list of habits for analytics/UI.
        - Delete habits from both memory and storage.
    """

    def __init__(self, storage: Storage):
        """
        Initialize the HabitManager and load all habits from storage.

        Args:
            storage (Storage): The storage backend (SQLite).
        """
        self.storage = storage
        self.habits = self.load_habits()

    def load_habits(self):
        """
        Load all habits and their completion timestamps from storage.

        Returns:
            list[Habit]: A list of fully reconstructed Habit objects.
        """
        habits = []
        for row in self.storage.fetch_habits():
            habit = Habit.from_db_row(row)
            completions = self.storage.fetch_completions(habit.id)
            habit.completions = [
                datetime.fromisoformat(ts[0]) for ts in completions
            ]
            habits.append(habit)
        return habits

    def create_habit(self, name: str, periodicity: str) -> Habit:
        """
        Create a new habit and save it to storage.

        Args:
            name (str): Name of the habit.
            periodicity (str): "daily" or "weekly".

        Returns:
            Habit: The newly created Habit instance.
        """
        habit_id = self.storage.insert_habit(name, periodicity, datetime.now())
        habit = Habit(name=name, periodicity=periodicity, id=habit_id)
        self.habits.append(habit)
        return habit

    def complete_habit(self, habit_id: int) -> bool:
        """
        Attempt to complete a habit.

        Returns:
            bool: True if completion succeeded, False if blocked.
        """
        habit = next(h for h in self.habits if h.id == habit_id)

        if habit.complete():
            # Save only if completion was allowed
            self.storage.insert_completion(habit_id, habit.completions[-1])
            return True

        return False

    def delete_habit(self, habit_id: int) -> None:
        """
        Delete a habit from memory and storage.
        """
        # Remove from SQLite
        self.storage.delete_habit(habit_id)

        # Remove from in-memory list
        self.habits = [h for h in self.habits if h.id != habit_id]
