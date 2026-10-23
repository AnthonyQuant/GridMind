# GridMind 🧠

GridMind is a professional-grade Tic-Tac-Toe application built entirely in Python. It features a modern flat-design GUI, persistent lifetime statistics, an unbeatable Minimax AI, and an advanced post-game analysis engine that evaluates your move decisions in hindsight.

## Features
* **Three Difficulty Levels:** Easy (Random), Medium (Tactical Heuristics), and Hard (Minimax Game-Tree Search).
* **Post-Game Analysis:** Replay matches step-by-step. The engine evaluates your moves and highlights tactical blunders or missed forced-wins with a visual indicator.
* **Persistent Statistics:** Tracks total games, win rates, and active win streaks against the CPU, saving data locally to JSON.
* **Modern GUI:** A responsive, multi-screen Tkinter interface utilizing a custom dark-slate color palette.
* **Automated Testing:** A complete `unittest` suite verifying engine rules, win detections, and AI logic independently of the graphical interface.

## Installation and Setup

GridMind runs on pure Python and requires no external third-party libraries. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AnthonyQuant/GridMind.git](https://github.com/AnthonyQuant/GridMind.git)
   cd GridMind