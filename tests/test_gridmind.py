import unittest
from tic_tac_toe_engine import TicTacToeEngine
import ai_engine
import game_analysis


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TicTacToeEngine()

    def test_winning_combinations(self):
        """Verifies that the engine correctly detects a win across a row."""
        self.engine.make_move(0, "X")
        self.engine.make_move(3, "O")
        self.engine.make_move(1, "X")
        self.engine.make_move(4, "O")
        game_over = self.engine.make_move(2, "X")

        self.assertTrue(game_over)
        self.assertEqual(self.engine.winner, "X")
        self.assertEqual(self.engine.winning_combination, (0, 1, 2))

    def test_occupied_cell_rejection(self):
        """Verifies the engine rejects moves on already filled squares."""
        self.engine.make_move(4, "X")
        with self.assertRaises(ValueError) as context:
            self.engine.make_move(4, "O")
        self.assertIn("already occupied", str(context.exception))

    def test_invalid_player_symbol(self):
        """Verifies that invalid player symbols like 'Z' are strictly rejected."""
        with self.assertRaises(ValueError):
            self.engine.make_move(0, "Z")

    def test_move_after_game_over(self):
        """Verifies the engine locks the board once a game is won."""
        self.engine.make_move(0, "X")
        self.engine.make_move(3, "O")
        self.engine.make_move(1, "X")
        self.engine.make_move(4, "O")
        self.engine.make_move(2, "X")  # X wins here

        with self.assertRaises(ValueError):
            self.engine.make_move(5, "O")


class TestAI(unittest.TestCase):
    def test_immediate_win(self):
        """Verifies the AI takes an immediate win when available."""
        board = ["X", "X", " ", "O", "O", " ", " ", " ", " "]
        move = ai_engine.get_ai_move(board, "Medium", "X")
        self.assertEqual(move, 2)

    def test_immediate_block(self):
        """Verifies the AI blocks an immediate human win."""
        board = ["X", "X", " ", " ", " ", " ", " ", " ", " "]
        move = ai_engine.get_ai_move(board, "Medium", "O")
        self.assertEqual(move, 2)

    def test_hard_ai_never_loses(self):
        """Verifies Hard AI correctly blocks a classic corner trap."""
        # Trap: X takes opposite corners (0, 8), O is in center (4).
        # X threatens to win on multiple fronts. O must pick an edge (1, 3, 5, 7) to force a block.
        board = ["X", " ", " ", " ", "O", " ", " ", " ", "X"]
        move = ai_engine.get_ai_move(board, "Hard", "O")
        self.assertIn(move, [1, 3, 5, 7])


class TestAnalysis(unittest.TestCase):
    def test_blunder_detection(self):
        """Verifies the advanced analysis correctly flags a fatal blunder."""
        # Human (X) is about to win if they play cell 2.
        # Instead, they play cell 8, throwing away the win and letting O win on cell 5.
        move_history = [
            {"player": "X", "cell": 0},
            {"player": "O", "cell": 3},
            {"player": "X", "cell": 1},
            {"player": "O", "cell": 4},
            {"player": "X", "cell": 8}  # The Blunder
        ]

        report = game_analysis.analyze_match(move_history)
        final_step = report[-1]

        self.assertIn("Blunder", final_step["feedback"])
        self.assertEqual(final_step["optimal_cell"], 2)


if __name__ == "__main__":
    unittest.main()