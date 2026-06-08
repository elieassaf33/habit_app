# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from manager import HabitManager
from analytics import (
    list_all,
    list_by_periodicity,
    longest_streak_all,
    longest_streak_for
)

class HabitTrackerUI:
    """
    Professional Tkinter UI for the Habit Tracking App.
    Clean layout, modern styling, and clear separation of concerns.
    """

    def __init__(self, root: tk.Tk, manager: HabitManager):
        self.root = root
        self.manager = manager

        self.root.title("Habit Tracker")
        self.root.geometry("850x650")
        self.root.configure(bg="#f5f5f5")

        self._configure_styles()
        self._build_layout()
        self._populate_habit_list()

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------

    def _configure_styles(self):
        """
        Configure modern ttk styles for a professional look.
        """
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=6)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_layout(self):
        """
        Build the main two-column layout.
        """
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left = ttk.Frame(container)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        ttk.Label(left, text="Your Habits", style="Header.TLabel").pack(anchor="w")

        self.habit_listbox = tk.Listbox(
            left, height=20, width=30, font=("Segoe UI", 10),
            bg="#ffffff", activestyle="none", highlightthickness=1,
            highlightbackground="#cccccc", selectbackground="#0078d7",
            selectforeground="white"
        )
        self.habit_listbox.pack(pady=8)
        self.habit_listbox.bind("<<ListboxSelect>>", self._on_select_habit)

        ttk.Button(left, text="Add Habit", style="Accent.TButton",
                   command=self._open_add_habit).pack(fill=tk.X, pady=3)
        ttk.Button(left, text="Complete Habit",
                   command=self._complete_selected).pack(fill=tk.X, pady=3)
        ttk.Button(left, text="Delete Habit",
                   command=self._delete_selected).pack(fill=tk.X, pady=3)
        ttk.Button(left, text="Analytics",
                   command=self._open_analytics_window).pack(fill=tk.X, pady=10)

        # Right panel
        right = ttk.Frame(container)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Habit Details", style="Header.TLabel").pack(anchor="w")

        self.details_text = tk.Text(
            right, height=20, width=60, font=("Segoe UI", 10),
            bg="#ffffff", relief="solid", borderwidth=1
        )
        self.details_text.pack(pady=8, fill=tk.BOTH, expand=True)
        self.details_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Habit List Handling
    # ------------------------------------------------------------------

    def _populate_habit_list(self):
        self.habit_listbox.delete(0, tk.END)
        for habit in self.manager.habits:
            self.habit_listbox.insert(tk.END, f"{habit.id}: {habit.name}")

    def _on_select_habit(self, event=None):
        selection = self.habit_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        habit = self.manager.habits[index]

        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)

        self.details_text.insert(tk.END, f"Name: {habit.name}\n")
        self.details_text.insert(tk.END, f"Periodicity: {habit.periodicity}\n")
        self.details_text.insert(tk.END, f"Created: {habit.created_at}\n")

        # NEW: show both current + record streak
        self.details_text.insert(tk.END, f"Current Streak: {habit.get_streak()}\n")
        self.details_text.insert(tk.END, f"Record Streak: {habit.get_record_streak()}\n\n")

        self.details_text.insert(tk.END, "Completions:\n")
        for ts in sorted(habit.completions, reverse=True):
            self.details_text.insert(tk.END, f" • {ts}\n")

        self.details_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Habit Actions
    # ------------------------------------------------------------------

    def _open_add_habit(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Habit")
        popup.geometry("300x200")
        popup.configure(bg="#f5f5f5")

        ttk.Label(popup, text="Habit Name:", style="Header.TLabel").pack(pady=5)
        name_entry = ttk.Entry(popup)
        name_entry.pack()

        ttk.Label(popup, text="Periodicity:", style="Header.TLabel").pack(pady=5)
        periodicity_box = ttk.Combobox(popup, values=["daily", "weekly"])
        periodicity_box.pack()

        def submit():
            name = name_entry.get()
            periodicity = periodicity_box.get()

            if not name or not periodicity:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            self.manager.create_habit(name, periodicity)
            self._populate_habit_list()
            popup.destroy()

        ttk.Button(popup, text="Create", style="Accent.TButton",
                   command=submit).pack(pady=15)

    def _complete_selected(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a habit first.")
            return

        index = selection[0]
        habit = self.manager.habits[index]

        success = self.manager.complete_habit(habit.id)

        if not success:
            msg = ("This habit is already completed today."
                   if habit.periodicity == "daily"
                   else "This habit is already completed this week.")
            messagebox.showinfo("Not allowed", msg)
            return

        self._on_select_habit()

    def _delete_selected(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a habit first.")
            return

        index = selection[0]
        habit = self.manager.habits[index]

        self.manager.storage.delete_habit(habit.id)
        self.manager.habits.remove(habit)

        self._populate_habit_list()
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Analytics Window
    # ------------------------------------------------------------------

    def _open_analytics_window(self):
        """
        Open a new window showing analytics results using pure functions.
        Includes:
            - All habits
            - Daily habits
            - Weekly habits
            - Longest daily streak overall
            - Longest weekly streak overall
            - Longest streak per habit
            - Longest streak for selected habit (if any)
        """
        win = tk.Toplevel(self.root)
        win.title("Analytics")
        win.geometry("550x600")
        win.configure(bg="#f5f5f5")

        text = tk.Text(
            win, state="normal", font=("Segoe UI", 10),
            bg="#ffffff", relief="solid", borderwidth=1
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        habits = self.manager.habits

        # ---------------------------------------------------------
        # All habits
        # ---------------------------------------------------------
        text.insert(tk.END, "All Habits:\n")
        for h in list_all(habits):
            text.insert(tk.END, f" • {h.name}\n")

        # ---------------------------------------------------------
        # Daily habits
        # ---------------------------------------------------------
        daily = list_by_periodicity(habits, "daily")
        text.insert(tk.END, "\nDaily Habits:\n")
        for h in daily:
            text.insert(tk.END, f" • {h.name}\n")

        # ---------------------------------------------------------
        # Weekly habits
        # ---------------------------------------------------------
        weekly = list_by_periodicity(habits, "weekly")
        text.insert(tk.END, "\nWeekly Habits:\n")
        for h in weekly:
            text.insert(tk.END, f" • {h.name}\n")

        # ---------------------------------------------------------
        # Longest daily streak overall (record streak)
        # ---------------------------------------------------------
        if daily:
            longest_daily = max(daily, key=lambda h: h.get_record_streak())
            text.insert(tk.END, "\nLongest Daily Streak Overall:\n")
            text.insert(
                tk.END,
                f" • {longest_daily.name}: {longest_daily.get_record_streak()}\n"
            )

        # ---------------------------------------------------------
        # Longest weekly streak overall (record streak)
        # ---------------------------------------------------------
        if weekly:
            longest_weekly = max(weekly, key=lambda h: h.get_record_streak())
            text.insert(tk.END, "\nLongest Weekly Streak Overall:\n")
            text.insert(
                tk.END,
                f" • {longest_weekly.name}: {longest_weekly.get_record_streak()}\n"
            )

        # ---------------------------------------------------------
        # Longest streak per habit (record streak)
        # ---------------------------------------------------------
        text.insert(tk.END, "\nLongest Streak Per Habit:\n")
        for h in habits:
            text.insert(tk.END, f" • {h.name}: {h.get_record_streak()}\n")

        # ---------------------------------------------------------
        # Longest streak for selected habit (record streak)
        # ---------------------------------------------------------
        selection = self.habit_listbox.curselection()
        if selection:
            selected = self.manager.habits[selection[0]]
            text.insert(tk.END, "\nLongest Streak For Selected Habit:\n")
            text.insert(
                tk.END,
                f" • {selected.name}: {selected.get_record_streak()}\n"
            )

        text.config(state="disabled")
