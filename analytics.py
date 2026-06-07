# analytics.py
"""
Pure functional analytics for the Habit Tracking App.

All functions in this module:
    - Are stateless
    - Have no side effects
    - Do not modify Habit objects
    - Do not access storage or UI
    - Operate only on the data passed to them

This ensures testability, predictability, and alignment with the
functional programming requirements of the assignment.
"""

def list_all(habits):
    return habits



def list_by_periodicity(habits, periodicity):
    return [h for h in habits if h.periodicity == periodicity]



def longest_streak_all(habits):
    if not habits:
        return None
    return max(habits, key=lambda h: h.get_streak())




def longest_streak_for(habits, name):
    matching = [h for h in habits if h.name == name]
    if not matching:
        return None
    return max(matching, key=lambda h: h.get_streak())
