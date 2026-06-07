# storage.py
import sqlite3
from datetime import datetime
from typing import List, Tuple

class Storage:
    """
    Handles all database operations for habits and completions.
    Uses SQLite for persistent storage.
    """

    def __init__(self, path="habits.db"):
        """
        Initialize the database connection and ensure tables exist.

        Args:
            path (str): Path to the SQLite database file.
        """
        self.conn = sqlite3.connect(path)
        self.init_db()

    def init_db(self) -> None:
        """
        Create the required tables if they do not already exist.
        """
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        """)

        self.conn.commit()

    def insert_habit(self, name: str, periodicity: str, created_at: datetime) -> int:
        """
        Insert a new habit into the database.

        Args:
            name (str): Habit name.
            periodicity (str): "daily" or "weekly".
            created_at (datetime): Creation timestamp.

        Returns:
            int: ID of the newly created habit.
        """
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)",
            (name, periodicity, created_at.isoformat())
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_completion(self, habit_id: int, timestamp: datetime) -> None:
        """
        Insert a completion timestamp for a habit.

        Args:
            habit_id (int): ID of the habit.
            timestamp (datetime): Completion timestamp.
        """
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
            (habit_id, timestamp.isoformat())
        )
        self.conn.commit()

    def fetch_habits(self) -> List[Tuple]:
        """
        Retrieve all habits from the database.

        Returns:
            List[Tuple]: Rows containing habit data.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, periodicity, created_at FROM habits")
        return cur.fetchall()

    def fetch_completions(self, habit_id: int) -> List[Tuple]:
        """
        Retrieve all completion timestamps for a habit.

        Args:
            habit_id (int): ID of the habit.

        Returns:
            List[Tuple]: Rows containing completion timestamps.
        """
        cur = self.conn.cursor()
        cur.execute(
            "SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at",
            (habit_id,)
        )
        return cur.fetchall()
    
    def delete_habit(self, habit_id: int) -> None:
        """
        Delete a habit and all its completion timestamps from the database.

        Args:
            habit_id (int): ID of the habit to delete.
        """
        cur = self.conn.cursor()

        # Delete completions first (foreign key constraint)
        cur.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

        # Delete the habit itself
        cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

        self.conn.commit()

