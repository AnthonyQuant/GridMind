import tkinter as tk
from tkinter import messagebox
from tic_tac_toe_engine import TicTacToeEngine
import arena_history
import game_analysis

# --- Design System ---
BG_COLOR = "#1A2A33"
CELL_BG = "#1F3641"
X_COLOR = "#31C3BD"
O_COLOR = "#F2B137"
TEXT_LIGHT = "#A8BFC9"
FONT_MAIN = ("Arial", 12, "bold")
FONT_LARGE = ("Arial", 28, "bold")
FONT_HUGE = ("Arial", 40, "bold")


class TicTacToeGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Arena")
        self.root.geometry("400x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.engine = TicTacToeEngine()
        self.mode = "VS CPU"
        self.current_match_moves = []
        self.current_difficulty = tk.StringVar(value="Hard")

        # Container for screen switching
        self.container = tk.Frame(self.root, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self._build_menu_screen()
        self._build_game_screen()
        self._build_stats_screen()

        self.show_screen("Menu")

    def show_screen(self, screen_name):
        """Hides all frames and raises the requested screen to the top."""
        if screen_name == "Stats":
            self._refresh_stats_ui()

        for frame in self.frames.values():
            frame.place_forget()
        self.frames[screen_name].place(relwidth=1, relheight=1)

    # ==========================================
    # SCREEN 1: MAIN MENU
    # ==========================================
    def _build_menu_screen(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        self.frames["Menu"] = frame

        logo_lbl = tk.Label(frame, text="X O", font=FONT_LARGE, bg=BG_COLOR, fg=X_COLOR)
        logo_lbl.pack(pady=(60, 30))

        card = tk.Frame(frame, bg=CELL_BG, bd=0, padx=20, pady=20)
        card.pack(fill="x", padx=30, pady=15)

        tk.Label(card, text="PICK PLAYER 1'S MARK", font=("Arial", 10, "bold"), bg=CELL_BG, fg=TEXT_LIGHT).pack(
            pady=(0, 15))
        tk.Label(card, text="REMEMBER: X GOES FIRST", font=("Arial", 9), bg=CELL_BG, fg=TEXT_LIGHT).pack(pady=(10, 0))

        # Interactive Difficulty Toggle
        diff_frame = tk.Frame(card, bg=CELL_BG)
        diff_frame.pack(pady=(15, 0))
        tk.Label(diff_frame, text="CPU DIFFICULTY:", font=("Arial", 9, "bold"), bg=CELL_BG, fg=TEXT_LIGHT).pack(
            side="left")

        diff_btn = tk.Button(diff_frame, textvariable=self.current_difficulty, font=("Arial", 9, "bold"),
                             bg=BG_COLOR, fg=X_COLOR, activebackground=BG_COLOR, activeforeground=X_COLOR,
                             relief="flat", width=8, command=self._toggle_difficulty)
        diff_btn.pack(side="left", padx=10)

        cpu_btn = tk.Button(frame, text="NEW GAME (VS CPU)", font=FONT_MAIN, bg=O_COLOR, fg=BG_COLOR,
                            activebackground="#FFC954", relief="flat", pady=15,
                            command=lambda: self.start_game("VS CPU"))
        cpu_btn.pack(fill="x", padx=30, pady=10)

        p2_btn = tk.Button(frame, text="NEW GAME (VS PLAYER)", font=FONT_MAIN, bg=X_COLOR, fg=BG_COLOR,
                           activebackground="#45E0D9", relief="flat", pady=15,
                           command=lambda: self.start_game("VS PLAYER"))
        p2_btn.pack(fill="x", padx=30, pady=5)

        stats_btn = tk.Button(frame, text="VIEW STATISTICS", font=FONT_MAIN, bg=TEXT_LIGHT, fg=BG_COLOR,
                              activebackground="#C0D5DF", relief="flat", pady=15,
                              command=lambda: self.show_screen("Stats"))
        stats_btn.pack(fill="x", padx=30, pady=10)

    def _toggle_difficulty(self):
        """Cycles through Easy, Medium, and Hard difficulty levels."""
        levels = ["Easy", "Medium", "Hard"]
        current = self.current_difficulty.get()
        next_idx = (levels.index(current) + 1) % len(levels)
        self.current_difficulty.set(levels[next_idx])

    def start_game(self, mode):
        self.mode = mode
        self.engine.set_difficulty(self.current_difficulty.get())
        self._next_round()
        self._update_scoreboard()
        self.show_screen("Game")

    # ==========================================
    # SCREEN 2: ACTIVE GAME BOARD
    # ==========================================
    def _build_game_screen(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        self.frames["Game"] = frame

        header = tk.Frame(frame, bg=BG_COLOR)
        header.pack(fill="x", padx=25, pady=(30, 20))

        tk.Label(header, text="X O", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=X_COLOR).pack(side="left")

        self.turn_lbl = tk.Label(header, text="X TURN", font=("Arial", 10, "bold"), bg=CELL_BG, fg=TEXT_LIGHT, padx=15,
                                 pady=5)
        self.turn_lbl.pack(side="left", expand=True)

        reset_btn = tk.Button(header, text="↻", font=("Arial", 14, "bold"), bg=TEXT_LIGHT, fg=BG_COLOR, relief="flat",
                              command=self._next_round)
        reset_btn.pack(side="right")

        self.board_frame = tk.Frame(frame, bg=BG_COLOR)
        self.board_frame.pack(pady=10)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=FONT_HUGE, width=3, height=1, bg=CELL_BG, fg=BG_COLOR,
                            activebackground=BG_COLOR, relief="flat", command=lambda idx=i: self._handle_click(idx))
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.buttons.append(btn)

        score_frame = tk.Frame(frame, bg=BG_COLOR)
        score_frame.pack(fill="x", padx=25, pady=20)

        self.x_score_lbl = tk.Label(score_frame, text="X (YOU)\n0", font=("Arial", 10, "bold"), bg=X_COLOR, fg=BG_COLOR,
                                    width=10, pady=8)
        self.x_score_lbl.pack(side="left", expand=True, padx=5)

        self.ties_score_lbl = tk.Label(score_frame, text="TIES\n0", font=("Arial", 10, "bold"), bg=TEXT_LIGHT,
                                       fg=BG_COLOR, width=10, pady=8)
        self.ties_score_lbl.pack(side="left", expand=True, padx=5)

        self.o_score_lbl = tk.Label(score_frame, text="O (CPU)\n0", font=("Arial", 10, "bold"), bg=O_COLOR, fg=BG_COLOR,
                                    width=10, pady=8)
        self.o_score_lbl.pack(side="left", expand=True, padx=5)

        self.result_overlay = tk.Frame(frame, bg=CELL_BG, pady=30)
        self.result_title = tk.Label(self.result_overlay, text="YOU WON!", font=("Arial", 10, "bold"), bg=CELL_BG,
                                     fg=TEXT_LIGHT)
        self.result_title.pack()
        self.result_subtitle = tk.Label(self.result_overlay, text="X TAKES THE ROUND", font=("Arial", 20, "bold"),
                                        bg=CELL_BG, fg=X_COLOR)
        self.result_subtitle.pack(pady=(10, 20))

        btn_box = tk.Frame(self.result_overlay, bg=CELL_BG)
        btn_box.pack()
        tk.Button(btn_box, text="QUIT", font=FONT_MAIN, bg=TEXT_LIGHT, fg=BG_COLOR, relief="flat", padx=10, pady=5,
                  command=lambda: self.show_screen("Menu")).pack(side="left", padx=10)
        tk.Button(btn_box, text="NEXT ROUND", font=FONT_MAIN, bg=O_COLOR, fg=BG_COLOR, relief="flat", padx=10, pady=5,
                  command=self._next_round).pack(side="left", padx=10)
        tk.Button(btn_box, text="REVIEW", font=FONT_MAIN, bg=X_COLOR, fg=BG_COLOR, relief="flat", padx=10, pady=5,
                  command=self._show_review).pack(side="left", padx=10)

    # ==========================================
    # SCREEN 3: PERSISTENT STATISTICS
    # ==========================================
    def _build_stats_screen(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        self.frames["Stats"] = frame

        tk.Label(frame, text="LIFETIME STATISTICS", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_LIGHT).pack(
            pady=(60, 20))

        self.stats_labels = {}
        stats_box = tk.Frame(frame, bg=CELL_BG, bd=0, padx=20, pady=20)
        stats_box.pack(fill="x", padx=30, pady=10)

        # UPDATED KEYS TO MATCH NEW ARENA HISTORY
        keys = [
            "Total games (All modes)",
            "VS CPU matches",
            "Human wins (VS CPU)",
            "AI wins (VS CPU)",
            "Draws (All modes)",
            "Win streak (VS CPU)",
            "Win rate (VS CPU)"
        ]
        for key in keys:
            row = tk.Frame(stats_box, bg=CELL_BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=key, font=("Arial", 11), bg=CELL_BG, fg=TEXT_LIGHT).pack(side="left")
            val_lbl = tk.Label(row, text="0", font=("Arial", 12, "bold"), bg=CELL_BG, fg=X_COLOR)
            val_lbl.pack(side="right")
            self.stats_labels[key] = val_lbl

        btn_box = tk.Frame(frame, bg=BG_COLOR)
        btn_box.pack(pady=30)

        tk.Button(btn_box, text="BACK TO MENU", font=FONT_MAIN, bg=TEXT_LIGHT, fg=BG_COLOR, relief="flat", padx=15,
                  pady=10, command=lambda: self.show_screen("Menu")).pack(side="left", padx=10)
        tk.Button(btn_box, text="RESET STATS", font=FONT_MAIN, bg="#f38ba8", fg=BG_COLOR, relief="flat", padx=15,
                  pady=10, command=self._intentional_stats_reset).pack(side="left", padx=10)

    def _refresh_stats_ui(self):
        stats = arena_history.get_calculated_stats()
        for key, lbl in self.stats_labels.items():
            lbl.config(text=str(stats.get(key, "0")))

    def _intentional_stats_reset(self):
        if messagebox.askyesno("Reset Statistics",
                               "Are you sure you want to permanently erase all persistent statistics?"):
            arena_history.reset_scoreboard()
            self._refresh_stats_ui()
            self._update_scoreboard()

    # ==========================================
    # GAME LOGIC & UI SYNC
    # ==========================================
    def _handle_click(self, index):
        if self.engine.game_over:
            return

        try:
            current_p = self.engine.current_player
            game_over = self.engine.make_move(index)
            self.current_match_moves.append({"player": current_p, "cell": index})
            self._update_board_ui()

            if game_over:
                self._finalize_match()
                return

            if self.mode == "VS CPU" and not game_over:
                # Now explicitly defaults to whatever difficulty is selected in the menu
                ai_move = self.engine.get_ai_move()
                if ai_move is not None:
                    ai_p = self.engine.current_player
                    game_over = self.engine.make_move(ai_move)
                    self.current_match_moves.append({"player": ai_p, "cell": ai_move})
                    self._update_board_ui()

                    if game_over:
                        self._finalize_match()
                        return
        except ValueError:
            pass

    def _update_board_ui(self):
        for i, symbol in enumerate(self.engine.board):
            color = X_COLOR if symbol == "X" else O_COLOR
            bg_color = CELL_BG

            if self.engine.game_over and i in self.engine.winning_combination:
                bg_color = color
                color = BG_COLOR

            self.buttons[i].config(text=symbol, fg=color, bg=bg_color)

        self.turn_lbl.config(text=f"{self.engine.current_player} TURN")

    def _update_scoreboard(self):
        data = arena_history.load_arena_data()
        stats = data.get("stats", {})

        o_label = "O (CPU)" if self.mode == "VS CPU" else "O (P2)"
        self.x_score_lbl.config(text=f"X (YOU)\n{stats.get('x_wins', 0)}")
        self.ties_score_lbl.config(text=f"TIES\n{stats.get('draws', 0)}")
        self.o_score_lbl.config(text=f"{o_label}\n{stats.get('o_wins', 0)}")

    def _finalize_match(self):
        winner = self.engine.winner
        arena_history.save_match_record(winner, self.mode, self.engine.difficulty, self.current_match_moves)
        self._update_scoreboard()
        self._update_board_ui()

        if winner in ["X", "O"]:
            self.result_title.config(text="PLAYER WINS!" if self.mode == "VS PLAYER" else (
                "YOU WON!" if winner == "X" else "OH NO, YOU LOST"))
            self.result_subtitle.config(text=f"{winner} TAKES THE ROUND", fg=X_COLOR if winner == "X" else O_COLOR)
        else:
            self.result_title.config(text="NOBODY WON")
            self.result_subtitle.config(text="ROUND TIED", fg=TEXT_LIGHT)

        self.result_overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=1)

    def _next_round(self):
        self.engine.reset_board()
        self.current_match_moves = []
        self.result_overlay.place_forget()
        self._update_board_ui()

    # ==========================================
    # GAME REVIEW / MATCH REPLAY MODULE
    # ==========================================
    def _show_review(self):
        """Opens the interactive Game Review window with step playback and move analysis."""
        if not self.current_match_moves:
            messagebox.showinfo("Game Review", "No move history available for this match!")
            return

        analysis = game_analysis.analyze_match(self.current_match_moves)

        review_win = tk.Toplevel(self.root)
        review_win.title("Tic-Tac-Toe Game Review")
        review_win.geometry("420x550")
        review_win.configure(bg=BG_COLOR)
        review_win.resizable(False, False)

        tk.Label(
            review_win, text="POST-GAME ANALYSIS", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=TEXT_LIGHT
        ).pack(pady=15)

        board_frame = tk.Frame(review_win, bg=BG_COLOR)
        board_frame.pack(pady=5)

        r_buttons = []
        for i in range(9):
            btn = tk.Label(board_frame, text="", font=FONT_LARGE, width=3, height=1, bg=CELL_BG)
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=5, pady=5)
            r_buttons.append(btn)

        feedback_lbl = tk.Label(
            review_win, text="Step 0 / " + str(len(analysis)), font=("Arial", 11),
            bg=BG_COLOR, fg=TEXT_LIGHT, wraplength=380, justify="center"
        )
        feedback_lbl.pack(pady=15)

        step_var = tk.IntVar(value=0)

        def render_step(step_idx):
            for b in r_buttons:
                b.config(bg=CELL_BG)

            if step_idx == 0:
                for b in r_buttons:
                    b.config(text="")
                feedback_lbl.config(text="Start of match. Click Next to review moves.")
                return

            step_data = analysis[step_idx - 1]
            board_state = step_data["board_state"]
            feedback_text = step_data["feedback"]

            for idx, symbol in enumerate(board_state):
                color = X_COLOR if symbol == "X" else (O_COLOR if symbol == "O" else BG_COLOR)
                r_buttons[idx].config(text=symbol, fg=color)

            played = step_data["played_cell"]
            r_buttons[played].config(bg="#2A4B5A")

            # --- VISUALLY HIGHLIGHT MISSED OPPORTUNITIES ---
            if "Blunder" in feedback_text or "Inaccurate" in feedback_text:
                optimal = step_data["optimal_cell"]
                # Show a subtle warning indicator on one of the optimal squares they SHOULD have played
                if optimal is not None and board_state[optimal] == " ":
                    r_buttons[optimal].config(text="?", fg="#E06C75", bg="#3E2A35")

            if step_idx == len(analysis) and self.engine.winner in ["X", "O"]:
                win_color = X_COLOR if self.engine.winner == "X" else O_COLOR
                for win_idx in self.engine.winning_combination:
                    r_buttons[win_idx].config(bg=win_color, fg=BG_COLOR)

            feedback_lbl.config(
                text=(f"Step {step_idx}/{len(analysis)} (Player {step_data['player']}):\n"
                      f"{feedback_text}")
            )

        def go_home():
            """Closes review popup, hides end-game overlay, and loads the Main Menu."""
            review_win.destroy()
            self.result_overlay.place_forget()
            self.show_screen("Menu")

        btn_frame = tk.Frame(review_win, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        def prev_step():
            if step_var.get() > 0:
                step_var.set(step_var.get() - 1)
                render_step(step_var.get())

        def next_step():
            if step_var.get() < len(analysis):
                step_var.set(step_var.get() + 1)
                render_step(step_var.get())

        tk.Button(btn_frame, text="◀ PREV", font=FONT_MAIN, bg=TEXT_LIGHT, fg=BG_COLOR, relief="flat", padx=10,
                  command=prev_step).pack(side="left", padx=5)

        # New HOME button directly inside the Review Window
        tk.Button(btn_frame, text="HOME", font=FONT_MAIN, bg=O_COLOR, fg=BG_COLOR, relief="flat", padx=10,
                  command=go_home).pack(side="left", padx=5)

        tk.Button(btn_frame, text="NEXT ▶", font=FONT_MAIN, bg=TEXT_LIGHT, fg=BG_COLOR, relief="flat", padx=10,
                  command=next_step).pack(side="left", padx=5)

        render_step(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()