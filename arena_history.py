import json
from pathlib import Path
from datetime import datetime

# Anchor storage file relative to this module's location
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "arena_history.json"


def get_default_data():
    """Returns the baseline structure for persistent statistics and match history."""
    return {
        "stats": {
            "total_games": 0,
            "cpu_matches": 0,  # Tracks total matches specifically against the CPU
            "x_wins": 0,
            "o_wins": 0,
            "human_wins": 0,
            "ai_wins": 0,
            "draws": 0,
            "current_win_streak": 0,
        },
        "matches": [],
    }


def load_arena_data():
    """Robustly loads match data. Will not crash on missing, empty, or corrupted files."""
    if not HISTORY_FILE.exists():
        return get_default_data()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "stats" not in data or "matches" not in data:
                return get_default_data()
            return data
    except (json.JSONDecodeError, OSError):
        return get_default_data()


def save_match_record(winner, mode, difficulty, move_history):
    """Calculates advanced metrics and saves the match to the JSON file."""
    data = load_arena_data()
    stats = data["stats"]

    stats["total_games"] = stats.get("total_games", 0) + 1

    # Basic generic tracking for the live scoreboard UI
    if winner == "X":
        stats["x_wins"] = stats.get("x_wins", 0) + 1
    elif winner == "O":
        stats["o_wins"] = stats.get("o_wins", 0) + 1

    if winner == "Draw":
        stats["draws"] = stats.get("draws", 0) + 1
        if mode == "VS CPU":
            stats["current_win_streak"] = 0

    # Advanced AI vs Human Tracking
    if mode == "VS CPU":
        stats["cpu_matches"] = stats.get("cpu_matches", 0) + 1
        if winner == "X":
            stats["human_wins"] = stats.get("human_wins", 0) + 1
            stats["current_win_streak"] = stats.get("current_win_streak", 0) + 1
        elif winner == "O":
            stats["ai_wins"] = stats.get("ai_wins", 0) + 1
            stats["current_win_streak"] = 0

    # Append structured match entry
    match_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "difficulty": difficulty if mode == "VS CPU" else "N/A",
        "winner": winner,
        "total_moves": len(move_history),
        "move_history": move_history,
    }
    data["matches"].append(match_entry)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as e:
        print(f"⚠️ OS Error saving arena history: {e}")


def get_calculated_stats():
    """Prepares the advanced statistics dictionary for the GUI to display."""
    data = load_arena_data()
    stats = data["stats"]

    total = stats.get("total_games", 0)
    cpu_total = stats.get("cpu_matches", 0)
    human = stats.get("human_wins", 0)

    # Win rate is strictly calculated using CPU matches. Draws count as non-wins.
    win_rate = 0.0
    if cpu_total > 0:
        win_rate = (human / cpu_total) * 100

    return {
        "Total games (All modes)": total,
        "VS CPU matches": cpu_total,
        "Human wins (VS CPU)": human,
        "AI wins (VS CPU)": stats.get("ai_wins", 0),
        "Draws (All modes)": stats.get("draws", 0),
        "Win streak (VS CPU)": stats.get("current_win_streak", 0),
        "Win rate (VS CPU)": f"{win_rate:.1f}%",
    }


def reset_scoreboard():
    """Intentionally resets cumulative session statistics while preserving match replays."""
    data = load_arena_data()
    data["stats"] = get_default_data()["stats"]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as e:
        print(f"⚠️ OS Error resetting scoreboard: {e}")