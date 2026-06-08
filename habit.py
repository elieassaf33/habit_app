# habit.py
from datetime import datetime
from typing import List

class Habit:
    """
    Represents a habit with a name, periodicity, creation date,
    and a list of completion timestamps.

    Attributes:
        id (int | None): Unique identifier in the database.
        name (str): Name of the habit (e.g., "Workout").
        periodicity (str): Frequency of the habit ("daily" or "weekly").
        created_at (datetime): Timestamp when the habit was created.
        completions (List[datetime]): List of timestamps when the habit was completed.
    """

    def __init__(self,
             id: int | None,
             name: str,
             periodicity: str,
             created_at: datetime | None = None,
             completions: List[datetime] | None = None):

        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.completions = completions or []


    def complete(self) -> bool:
        """
        Record a completion timestamp if allowed.

        Daily habits:
            - Can only be completed once per calendar day.

        Weekly habits:
            - Can only be completed once per ISO calendar week.

        Returns:
            bool: True if completion was added, False if blocked.
        """
        now = datetime.now()

        if self.completions:
            last = self.completions[-1]

            if self.periodicity == "daily":
                # Same calendar day → block
                if last.date() == now.date():
                    return False

            elif self.periodicity == "weekly":
                # Same ISO week → block
                last_year, last_week, _ = last.isocalendar()
                now_year, now_week, _ = now.isocalendar()
                if last_year == now_year and last_week == now_week:
                    return False

        # Add completion and return True
        self.completions.append(now)
        return True


    def get_streak(self) -> int:
        if not self.completions:
            return 0

        period = self.periodicity.lower()

        # normalize to dates first (CRITICAL FIX)
        if period == "daily":
            days = sorted({c.date() for c in self.completions}, reverse=True)

            streak = 1
            for i in range(1, len(days)):
                if (days[i - 1] - days[i]).days == 1:
                    streak += 1
                else:
                    break
            return streak

        if period == "weekly":
            weeks = sorted(
                {(c.isocalendar().year, c.isocalendar().week) for c in self.completions},
                reverse=True
            )

            streak = 1
            for i in range(1, len(weeks)):
                prev_year, prev_week = weeks[i - 1]
                curr_year, curr_week = weeks[i]

                # proper week adjacency handling
                if (prev_year == curr_year and prev_week - curr_week == 1) or \
                (prev_year - curr_year == 1 and prev_week == 1 and curr_week >= 52):
                    streak += 1
                else:
                    break

            return streak

        return 0



    @classmethod
    def from_db_row(cls, row):
        """
        Reconstruct a Habit object from a database row.

        Args:
            row (tuple): (id, name, periodicity, created_at)

        Returns:
            Habit: A Habit instance with empty completions (to be filled later).
        """
        habit_id, name, periodicity, created_at_str = row
        created_at = datetime.fromisoformat(created_at_str)
        return cls(name=name, periodicity=periodicity,
                   id=habit_id, created_at=created_at)

    def get_record_streak(self) -> int:
        if not self.completions:
            return 0

        # Normalize dates or weeks depending on periodicity
        if self.periodicity == "daily":
            dates = sorted({c.date() for c in self.completions})
            max_streak = 1
            current = 1

            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
                    current += 1
                else:
                    max_streak = max(max_streak, current)
                    current = 1

            return max(max_streak, current)

        if self.periodicity == "weekly":
            weeks = sorted(
                {(c.isocalendar().year, c.isocalendar().week) for c in self.completions}
            )
            max_streak = 1
            current = 1

            for i in range(1, len(weeks)):
                prev_year, prev_week = weeks[i - 1]
                year, week = weeks[i]

                # consecutive week logic
                if (year == prev_year and week - prev_week == 1) or \
                (year - prev_year == 1 and prev_week == 52 and week == 1):
                    current += 1
                else:
                    max_streak = max(max_streak, current)
                    current = 1

            return max(max_streak, current)

        return 0
