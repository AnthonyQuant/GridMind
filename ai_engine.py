import random

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


def check_win(board, player):
  """Evaluates if the specified player has achieved a winning line on the board."""
  for combo in WINNING_COMBINATIONS:
    if all(board[i] == player for i in combo):
      return True
  return False


def get_ai_move(board, difficulty, ai_player):
  """Main entry point to select AI move based on difficulty setting.

  Args:
      board (list): 9-element list representing 3x3 board ('X', 'O', or ' ').
      difficulty (str): 'Easy', 'Medium', or 'Hard'.
      ai_player (str): 'X' or 'O'.

  Returns:
      int: Selected board cell index (0-8).
  """
  empty_cells = [i for i, cell in enumerate(board) if cell == " "]
  if not empty_cells:
    return None

  human_player = "X" if ai_player == "O" else "O"

  # 1. Easy Mode: Pure Random Selection
  if difficulty == "Easy":
    return random.choice(empty_cells)

  # 2. Medium Mode: Tactical Heuristics (Win -> Block -> Center -> Random)
  if difficulty == "Medium":
    # Immediate Win Check
    for cell in empty_cells:
      board[cell] = ai_player
      if check_win(board, ai_player):
        board[cell] = " "
        return cell
      board[cell] = " "

    # Immediate Block Check
    for cell in empty_cells:
      board[cell] = human_player
      if check_win(board, human_player):
        board[cell] = " "
        return cell
      board[cell] = " "

    # Take Center
    if board[4] == " ":
      return 4

    return random.choice(empty_cells)

  # 3. Hard Mode: Unbeatable Minimax Game-Tree Search
  best_score = -float("inf")
  best_move = random.choice(empty_cells)

  for cell in empty_cells:
    board[cell] = ai_player
    score = minimax(board, depth=0, is_maximizing=False, ai_player=ai_player, human_player=human_player)
    board[cell] = " "
    if score > best_score:
      best_score = score
      best_move = cell

  return best_move


def minimax(board, depth, is_maximizing, ai_player, human_player):
  """Recursive Minimax algorithm to evaluate possible board outcomes.

  Scores outcomes as:
  - AI Win: +(10 - depth)
  - Human Win: -(10 - depth)
  - Draw: 0
  """
  if check_win(board, ai_player):
    return 10 - depth
  if check_win(board, human_player):
    return depth - 10
  if " " not in board:
    return 0

  if is_maximizing:
    best_score = -float("inf")
    for i in range(9):
      if board[i] == " ":
        board[i] = ai_player
        score = minimax(board, depth + 1, False, ai_player, human_player)
        board[i] = " "
        best_score = max(score, best_score)
    return best_score
  else:
    best_score = float("inf")
    for i in range(9):
      if board[i] == " ":
        board[i] = human_player
        score = minimax(board, depth + 1, True, ai_player, human_player)
        board[i] = " "
        best_score = min(score, best_score)
    return best_score