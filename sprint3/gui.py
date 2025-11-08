"""
Hashim Abdulla
SOS Game GUI Module - Sprint 3
Updated to work with class hierarchy and display game results
"""

import tkinter as tk
from tkinter import messagebox
from game_logic import create_game, SOSGame


class SOSGUI:
    """Main GUI class for SOS Game"""

    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game - Sprint 3")
        self.game = None  # Will be created when game starts

        # GUI state
        self.board_buttons = []
        self.blue_letter_var = tk.StringVar(value='S')
        self.red_letter_var = tk.StringVar(value='S')
        self.sos_lines = []  # Store drawn SOS lines for visualization

        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Top frame for game settings
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack()

        # Title
        title_label = tk.Label(top_frame, text="SOS - by Hashim Abdulla", font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Game mode selection
        mode_frame = tk.Frame(top_frame)
        mode_frame.grid(row=1, column=0, columnspan=3, pady=5)

        self.mode_var = tk.StringVar(value=SOSGame.SIMPLE_MODE)
        simple_radio = tk.Radiobutton(mode_frame, text="Simple game",
                                      variable=self.mode_var,
                                      value=SOSGame.SIMPLE_MODE)
        simple_radio.pack(side=tk.LEFT, padx=10)

        general_radio = tk.Radiobutton(mode_frame, text="General game",
                                       variable=self.mode_var,
                                       value=SOSGame.GENERAL_MODE)
        general_radio.pack(side=tk.LEFT, padx=10)

        # Board size selection
        size_frame = tk.Frame(top_frame)
        size_frame.grid(row=2, column=0, columnspan=3, pady=5)

        tk.Label(size_frame, text="Board size:").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value='3')
        size_spinbox = tk.Spinbox(size_frame, from_=3, to=10, width=5,
                                  textvariable=self.size_var)
        size_spinbox.pack(side=tk.LEFT, padx=5)

        # New Game button
        new_game_btn = tk.Button(top_frame, text="New Game",
                                 command=self.start_new_game,
                                 bg='lightgreen', font=('Arial', 12, 'bold'))
        new_game_btn.grid(row=3, column=0, columnspan=3, pady=10)

        # Main game frame
        game_frame = tk.Frame(self.root)
        game_frame.pack(pady=10)

        # Left panel - Blue player
        left_panel = tk.Frame(game_frame, width=150)
        left_panel.grid(row=0, column=0, padx=10, sticky='n')

        tk.Label(left_panel, text="Blue player", fg='blue',
                 font=('Arial', 14, 'bold')).pack(pady=10)

        blue_s = tk.Radiobutton(left_panel, text="S", variable=self.blue_letter_var,
                                value='S', font=('Arial', 12))
        blue_s.pack(anchor='w')

        blue_o = tk.Radiobutton(left_panel, text="O", variable=self.blue_letter_var,
                                value='O', font=('Arial', 12))
        blue_o.pack(anchor='w')

        # Blue score label
        self.blue_score_label = tk.Label(left_panel, text="Score: 0",
                                         fg='blue', font=('Arial', 12))
        self.blue_score_label.pack(pady=10)

        # Center - Board
        self.board_frame = tk.Frame(game_frame, bg='white')
        self.board_frame.grid(row=0, column=1, padx=20)

        # Right panel - Red player
        right_panel = tk.Frame(game_frame, width=150)
        right_panel.grid(row=0, column=2, padx=10, sticky='n')

        tk.Label(right_panel, text="Red player", fg='red',
                 font=('Arial', 14, 'bold')).pack(pady=10)

        red_s = tk.Radiobutton(right_panel, text="S", variable=self.red_letter_var,
                               value='S', font=('Arial', 12))
        red_s.pack(anchor='w')

        red_o = tk.Radiobutton(right_panel, text="O", variable=self.red_letter_var,
                               value='O', font=('Arial', 12))
        red_o.pack(anchor='w')

        # Red score label
        self.red_score_label = tk.Label(right_panel, text="Score: 0",
                                        fg='red', font=('Arial', 12))
        self.red_score_label.pack(pady=10)

        # Bottom - Turn indicator
        self.turn_label = tk.Label(self.root, text="Click 'New Game' to start",
                                   font=('Arial', 14))
        self.turn_label.pack(pady=10)

        # Create initial board
        self.create_board_display(3)

    def validate_board_size(self):
        """Validate the board size input"""
        try:
            size = int(self.size_var.get())
            if not (3 <= size <= 10):
                messagebox.showerror("Invalid Input",
                                     "Board size must be between 3 and 10")
                return None
            return size
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Board size must be a number between 3 and 10")
            return None

    def start_new_game(self):
        """Start a new game with selected settings"""
        # Validate board size
        size = self.validate_board_size()
        if size is None:
            return

        try:
            mode = self.mode_var.get()
            self.game = create_game(mode)
            self.game.set_board_size(size)
            self.game.start_new_game()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Update GUI
        self.create_board_display(size)
        self.update_turn_label()
        self.update_scores()
        messagebox.showinfo("New Game",
                            f"New {self.game.game_mode} game started!\nBoard size: {size}x{size}")

    def create_board_display(self, size):
        """Create the board grid of buttons"""
        # Clear existing board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board_buttons = []

        for row in range(size):
            button_row = []
            for col in range(size):
                btn = tk.Button(self.board_frame, text=' ',
                                width=4, height=2,
                                font=('Arial', 18, 'bold'),
                                bg='white',
                                command=lambda r=row, c=col: self.on_cell_click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.board_buttons.append(button_row)

    def on_cell_click(self, row, col):
        """Handle cell click event"""
        if self.game is None or not self.game.game_started:
            messagebox.showwarning("Game Not Started", "Please start a new game first")
            return

        if self.game.is_game_over():
            messagebox.showinfo("Game Over", "Game has ended. Start a new game to play again.")
            return

        # Get the current player's selected letter
        current_player = self.game.get_current_player()
        if current_player.color == 'blue':
            letter = self.blue_letter_var.get()
        else:
            letter = self.red_letter_var.get()

        # Try to make the move
        try:
            self.game.make_move(row, col, letter)

            # Update the button display
            self.board_buttons[row][col].config(
                text=letter,
                fg=current_player.color,
                state='disabled'
            )

            # Update scores
            self.update_scores()

            # Check if game is over
            if self.game.is_game_over():
                self.display_game_result()
            else:
                # Update turn label
                self.update_turn_label()

        except ValueError as e:
            messagebox.showerror("Invalid Move", str(e))
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))

    def update_turn_label(self):
        """Update the turn indicator label"""
        if self.game is None:
            return

        current_player = self.game.get_current_player()
        self.turn_label.config(
            text=f"Current turn: {current_player.name.lower()}",
            fg=current_player.color
        )

    def update_scores(self):
        """Update score labels"""
        if self.game is None:
            return

        self.blue_score_label.config(text=f"Score: {self.game.blue_player.score}")
        self.red_score_label.config(text=f"Score: {self.game.red_player.score}")

    def display_game_result(self):
        """Display the game result when game is over"""
        winner = self.game.get_winner()

        if winner == "Draw":
            if self.game.game_mode == SOSGame.SIMPLE_MODE:
                message = "Game Over!\n\nResult: Draw\n\nThe board is full with no SOS formed."
            else:
                message = f"Game Over!\n\nResult: Draw\n\nBoth players scored {self.game.blue_player.score} points!"
            self.turn_label.config(text="Game ended in a draw", fg='black')
        else:
            if self.game.game_mode == SOSGame.SIMPLE_MODE:
                message = f"Game Over!\n\n{winner.name} player wins!\n\n{winner.name} formed the first SOS!"
            else:
                blue_score = self.game.blue_player.score
                red_score = self.game.red_player.score
                message = f"Game Over!\n\n{winner.name} player wins!\n\nBlue: {blue_score} | Red: {red_score}"

            self.turn_label.config(text=f"{winner.name} player wins!", fg=winner.color)

        messagebox.showinfo("Game Over", message)


def main():
    """Main entry point for the applicatiton"""
    root = tk.Tk()
    app = SOSGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()