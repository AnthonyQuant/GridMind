import random

import ai_engine

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),  # Rows
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),  # Columns
    (0, 4, 8),
    (2, 4, 6),  # Diagonals
]


class TicTacToeEngine:

  def __init__(self, default_difficulty="Hard"):
    self.board = [" " for _ in range(9)]
    self.current_player = "X"
    self.winner = None
    self.winning_combination = []
    self.game_over = False
    # 1. State tracking for AI difficulty
    self.difficulty = default_difficulty

  def set_difficulty(self, difficulty_level):
    """Updates the engine's default AI difficulty setting."""
    if difficulty_level in ["Easy", "Medium", "Hard"]:
      self.difficulty = difficulty_level

  def reset_board(self):
    """Resets round state while maintaining persistent score and difficulty settings."""
    self.board = [" " for _ in range(9)]
    self.current_player = "X"
    self.winner = None
    self.winning_combination = []
    self.game_over = False

  def make_move(self, index, player=None):
      """Executes a move and checks for game completion, enforcing strict game rules."""
      if self.game_over:
          raise ValueError("Game is already over. Start a new round!")
      if type(index) is not int or index < 0 or index > 8:
          raise ValueError("Invalid board index. Must be an integer between 0 and 8.")
      if self.board[index] != " ":
          raise ValueError("Cell is already occupied!")

      # Determine which player is making the move
      active_player = player if player else self.current_player

      # --- NEW: VALIDATE PLAYER SYMBOL ---
      if active_player not in ["X", "O"]:
          raise ValueError(f"Invalid player symbol: '{active_player}'. Must be 'X' or 'O'.")

      # --- NEW: ENFORCE TURN ORDER ---
      if active_player != self.current_player:
          raise ValueError(f"Out of turn: It is currently Player {self.current_player}'s turn.")

      # Apply the move
      self.board[index] = active_player

      # Check outcomes
      if self._check_win(active_player):
          self.winner = active_player
          self.game_over = True
      elif " " not in self.board:
          self.winner = "Draw"
          self.game_over = True
      else:
          # Swap turns
          self.current_player = "O" if self.current_player == "X" else "X"

      return self.game_over

  def _check_win(self, player):
    for combo in WINNING_COMBINATIONS:
      if all(self.board[i] == player for i in combo):
        self.winning_combination = combo
        return True
    return False

  def get_ai_move(self, difficulty=None):
    """Determines AI move using the specified difficulty override or active engine setting."""
    target_difficulty = difficulty if difficulty else self.difficulty
    # 2. Delegates to ai_engine.py based on target_difficulty
    return ai_engine.get_ai_move(
        self.board, target_difficulty, self.current_player
    )

  def _minimax(self, board, depth, is_maximizing, ai_player, human_player):
    """Recursive minimax game-tree evaluation function."""
    if self._check_virtual_win(board, ai_player):
      return 10 - depth
    if self._check_virtual_win(board, human_player):
      return depth - 10
    if " " not in board:
      return 0

    if is_maximizing:
      best_score = -float("inf")
      for i in range(9):
        if board[i] == " ":
          board[i] = ai_player
          score = self._minimax(board, depth + 1, False, ai_player, human_player)
          board[i] = " "
          best_score = max(score, best_score)
      return best_score
    else:
      best_score = float("inf")
      for i in range(9):
        if board[i] == " ":
          board[i] = human_player
          score = self._minimax(board, depth + 1, True, ai_player, human_player)
          board[i] = " "
          best_score = min(score, best_score)
      return best_score

  def _check_virtual_win(self, board, player):
    """Helper for minimax to evaluate board states without mutating main state."""
    for combo in WINNING_COMBINATIONS:
      if all(board[i] == player for i in combo):
        return True
    return False