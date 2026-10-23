"""game_analysis.py - Advanced Post-Game Analysis Engine"""

import ai_engine

def evaluate_move(board, cell, player):
    """Returns the absolute minimax score of a specific move."""
    opponent = "O" if player == "X" else "X"
    board[cell] = player

    # Check immediate outcomes
    if ai_engine.check_win(board, player):
        score = 10
    elif " " not in board:
        score = 0
    else:
        # Simulate opponent's optimal response (minimizing player's score)
        score = ai_engine.minimax(board, 1, False, player, opponent)

    board[cell] = " "
    return score

def analyze_match(move_history):
    """Evaluates the actual move vs the best available moves using Minimax."""
    board = [" " for _ in range(9)]
    analysis_report = []

    for step_num, move in enumerate(move_history, 1):
        player = move["player"]
        played_cell = move["cell"]
        empty_cells = [i for i, spot in enumerate(board) if spot == " "]

        # 1. Score all available moves to find the true optimal outcome
        best_score = -float("inf")
        best_moves = []
        for cell in empty_cells:
            score = evaluate_move(board, cell, player)
            if score > best_score:
                best_score = score
                best_moves = [cell]
            elif score == best_score:
                # Treat all moves with the same optimal value as equally good
                best_moves.append(cell)

        # 2. Score the actual move the human played
        played_score = evaluate_move(board, played_cell, player)

        # 3. Generate precise feedback based on outcome differences
        feedback = "Good move."
        if played_score < best_score:
            if best_score > 0 and played_score == 0:
                feedback = "⚠️ Blunder! You missed a forced win and allowed a draw."
            elif best_score > 0 and played_score < 0:
                feedback = "⚠️ Fatal Blunder! You went from a forced win to a forced loss."
            elif best_score == 0 and played_score < 0:
                feedback = "⚠️ Blunder! You threw away a guaranteed draw and allowed a forced loss."
            elif best_score > 0 and played_score > 0:
                feedback = "⚠️ Inaccurate. You still have a forced win, but missed a faster victory."
            else:
                feedback = "⚠️ Suboptimal move. There were better options available."
        elif best_score < 0:
             feedback = "The opponent has a forced win regardless of this move."

        # Pick one of the optimal cells to highlight (if they didn't pick one)
        optimal_highlight = best_moves[0] if played_cell not in best_moves else None

        # Apply the move to progress the game state
        board[played_cell] = player

        analysis_report.append({
            "step": step_num,
            "player": player,
            "played_cell": played_cell,
            "optimal_cell": optimal_highlight,
            "feedback": feedback,
            "board_state": list(board),
        })

    return analysis_report