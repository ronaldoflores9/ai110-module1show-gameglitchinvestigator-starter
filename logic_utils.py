#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
import json
import os

HIGH_SCORE_FILE = "high_score.json"


def load_high_score(filepath: str = HIGH_SCORE_FILE) -> dict:
    """
    Load the high score table from a JSON file.

    Returns a dict keyed by difficulty, e.g. {"Easy": 90, "Normal": 70}.
    Returns an empty dict if the file does not exist or is invalid.
    """
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_high_score(score: int, difficulty: str, filepath: str = HIGH_SCORE_FILE) -> bool:
    """
    Save a new score for the given difficulty if it beats the current record.

    Returns True if a new high score was set, False otherwise.
    """
    table = load_high_score(filepath)
    if score > table.get(difficulty, 0):
        table[difficulty] = score
        try:
            with open(filepath, "w") as f:
                json.dump(table, f)
            return True
        except OSError:
            return False
    return False

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            float_val = float(raw)
            if float_val != int(float_val):
                return False, None, f"Please enter a whole number (e.g. {int(float_val)} or {int(float_val) + 1})."
            value = int(float_val)
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
