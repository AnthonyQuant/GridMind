# GridMind 🧠

GridMind is a professional-grade Tic-Tac-Toe application built entirely in Python. It features a modern flat-design GUI, persistent lifetime statistics, an unbeatable Minimax AI, and an advanced post-game analysis engine that evaluates your move decisions in hindsight.

## 📸 Screenshots
*(Add images here by replacing the links)*
![Main Menu](link-to-menu-image)
![Gameplay](link-to-gameplay-image)
![Game Review Analysis](link-to-review-image)

## 🚀 Installation and Setup

GridMind runs on pure Python and requires no external third-party libraries.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AnthonyQuant/GridMind.git](https://github.com/AnthonyQuant/GridMind.git)
   cd GridMind
   ```

2. **Launch the Game:**
   ```bash
   python GUI.py
   ```
   *(Note: Linux users may need to install `python3-tk` via their package manager if Tkinter is not bundled with their Python distribution).*

3. **Run the Automated Tests:**
   ```bash
   python -m unittest tests/test_gridmind.py
   ```

## 🎮 Controls

* **Mouse Clicks:** The entire application is driven by an intuitive point-and-click graphical interface. Click the main menu buttons to select your game mode and CPU difficulty. 
* **Gameplay:** Click any empty square on the 3x3 grid to place your 'X' or 'O'. 
* **Review Mode:** Use the "PREV" and "NEXT" buttons to step through historical moves, or "HOME" to return to the main menu.

## 🧠 How the AI Works

### Minimax Algorithm (Hard Difficulty)
The "Hard" CPU opponent uses the **Minimax** algorithm, a recursive game-tree search that looks ahead at every possible future move until the game reaches a terminal state (win, loss, or draw). 
It scores these terminal states (+10 for an AI win, -10 for a human win, 0 for a draw) and passes the scores back up the tree. The AI assumes the human player will always play optimally to minimize the AI's score, so it selects the move that maximizes its worst-case scenario. Because Tic-Tac-Toe is a solved game, Minimax guarantees the AI will never lose.

### Advanced Post-Game Move Analysis
When you click "Review" after a match, the `game_analysis.py` engine evaluates your actual played moves against the absolute optimal moves determined by Minimax.
1. The engine scans the historical board state on your turn.
2. It scores every available empty square using Minimax to find the best possible outcome.
3. It scores the square you *actually* chose.
4. If your move resulted in a mathematically worse outcome (e.g., you threw away a guaranteed draw to allow a forced loss, or missed an instant win), the engine flags it as a **Blunder** or **Inaccurate** and places a red `?` on the board to show you the square you should have picked.

## Architecture
GridMind follows a modular design pattern, separating the user interface (`GUI.py`) from the game rules (`tic_tac_toe_engine.py`), the decision algorithms (`ai_engine.py`), and the performance tracking (`arena_history.py` and `game_analysis.py`).