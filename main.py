# main.py
"""
Entry point for the Habit Tracking App.

This module initializes:
    - The SQLite storage backend
    - The HabitManager (business logic)
    - The Tkinter graphical user interface

Running this file starts the full application.
"""

import tkinter as tk
from storage import Storage
from manager import HabitManager
from ui import HabitTrackerUI
from fixtures import load_fixtures

def main():
    """
    Start the Habit Tracking application.

    This function:
        1. Creates the SQLite storage.
        2. Loads all habits via HabitManager.
        3. Launches the Tkinter UI.
    """
    # Initialize storage and manager
    storage = Storage()
    manager = HabitManager(storage)

    # Load predefined habits + 4 weeks of data
    load_fixtures(storage, manager)

    # Initialize Tkinter root window
    root = tk.Tk()

    # Launch the UI
    HabitTrackerUI(root, manager)

    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
