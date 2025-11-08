"""
Hashim Abdulla
SOS Game Logic Module - Sprint 3 increment
Includes class hierarchy for Simple and General game modes
Detects SOS sequences and determines game winners
"""


class GameBoard:
    """Represents the SOS game board"""

    def __init__(self, size=3):
        if not self.is_valid_size(size):
            raise ValueError("Board size must be between 3 and 10")
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    @staticmethod
    def is_valid_size(size):
        """Validate board size is between 3 and 10"""
        return 3 <= size <= 10

    def is_cell_empty(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        return self.grid[row][col] == ' '

    def place_letter(self, row, col, letter):
        if not self.is_cell_empty(row, col):
            raise ValueError("Cell is already occupied")
        if letter not in ['S', 'O']:
            raise ValueError("Letter must be S or O")
        self.grid[row][col] = letter

    def get_cell(self, row, col):
        return self.grid[row][col]

    def is_board_full(self):
        """Check if the board is completely filled"""
        for row in self.grid:
            if ' ' in row:
                return False
        return True

    def reset(self):
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]

    def check_sos_at_position(self, row, col):
        sequences = []

        # All 8 directions: horizontal, vertical, and 4 diagonals
        directions = [
            (0, 1),  # Horizontal right
            (1, 0),  # Vertical down
            (1, 1),  # Diagonal down-right
            (1, -1),  # Diagonal down-left
        ]

        for dr, dc in directions:
            # Check if this cell is 'S' (start of SOS)
            if self.get_cell(row, col) == 'S':
                # Check forward: S-O-S
                if self._is_valid_position(row + dr, col + dc) and \
                        self._is_valid_position(row + 2 * dr, col + 2 * dc):
                    if self.get_cell(row + dr, col + dc) == 'O' and \
                            self.get_cell(row + 2 * dr, col + 2 * dc) == 'S':
                        sequences.append([
                            (row, col),
                            (row + dr, col + dc),
                            (row + 2 * dr, col + 2 * dc)
                        ])

            # Check if this cell is 'O' (middle of SOS)
            if self.get_cell(row, col) == 'O':
                # Check both directions: S-O-S
                if self._is_valid_position(row - dr, col - dc) and \
                        self._is_valid_position(row + dr, col + dc):
                    if self.get_cell(row - dr, col - dc) == 'S' and \
                            self.get_cell(row + dr, col + dc) == 'S':
                        sequences.append([
                            (row - dr, col - dc),
                            (row, col),
                            (row + dr, col + dc)
                        ])

            # Check if this cell is 'S' (end of SOS)
            if self.get_cell(row, col) == 'S':
                # Check backward: S-O-S
                if self._is_valid_position(row - dr, col - dc) and \
                        self._is_valid_position(row - 2 * dr, col - 2 * dc):
                    if self.get_cell(row - dr, col - dc) == 'O' and \
                            self.get_cell(row - 2 * dr, col - 2 * dc) == 'S':
                        sequences.append([
                            (row - 2 * dr, col - 2 * dc),
                            (row - dr, col - dc),
                            (row, col)
                        ])

        return sequences

    def _is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.size and 0 <= col < self.size


class Player:
    """Represents a player in the game"""

    def __init__(self, name, color):
        """Initialize player with name and color"""
        self.name = name
        self.color = color  # 'blue' or 'red'
        self.score = 0

    def reset_score(self):
        self.score = 0

    def add_score(self, points=1):
        """Add points to player's score"""
        self.score += points



class SOSGame:

    SIMPLE_MODE = "Simple"
    GENERAL_MODE = "General"

    def __init__(self):
        self.board = None
        self.board_size = 3
        self.blue_player = Player("Blue", "blue")
        self.red_player = Player("Red", "red")
        self.current_player = self.blue_player
        self.game_started = False
        self.game_over = False
        self.winner = None  # Can be blue_player, red_player, or "Draw"

    def set_board_size(self, size):
        if not GameBoard.is_valid_size(size):
            raise ValueError("Board size must be between 3 and 10")
        self.board_size = size

    def start_new_game(self):
        """Initialize a new game - common for both modes"""
        self.board = GameBoard(self.board_size)
        self.current_player = self.blue_player
        self.blue_player.reset_score()
        self.red_player.reset_score()
        self.game_started = True
        self.game_over = False
        self.winner = None

    def make_move(self, row, col, letter):

        if not self.game_started:
            raise RuntimeError("Game has not been started")

        if self.game_over:
            raise RuntimeError("Game is already over")

        if not self.board.is_cell_empty(row, col):
            raise ValueError("Cell is already occupied")

        # Place the letter
        self.board.place_letter(row, col, letter)

        # Check for SOS sequences formed by this move
        sos_sequences = self.board.check_sos_at_position(row, col)

        # Handle SOS sequences (different for Simple vs General)
        sos_found = len(sos_sequences) > 0
        self.handle_sos_found(sos_found, sos_sequences)

        # Check if game is over (different for Simple vs General)
        self.check_game_over()

        # Switch turns if appropriate (different for Simple vs General)
        if not self.game_over:
            self.handle_turn_switch(sos_found)

    def handle_sos_found(self, sos_found, sequences):

        raise NotImplementedError("Subclasses must implement handle_sos_found()")

    def check_game_over(self):

        raise NotImplementedError("Subclasses must implement check_game_over()")

    def handle_turn_switch(self, sos_found):

        raise NotImplementedError("Subclasses must implement handle_turn_switch()")

    def switch_turn(self):
        """Switch to the other player"""
        if self.current_player == self.blue_player:
            self.current_player = self.red_player
        else:
            self.current_player = self.blue_player

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner


"""Simple Game Mode: First SOS wins"""


class SimpleGame(SOSGame):
    """
    Simple game mode implementation
    - First player to form SOS wins immediately
    - Draw if board fills with no SOS
    """

    def __init__(self):
        super().__init__()
        self.game_mode = self.SIMPLE_MODE

    def handle_sos_found(self, sos_found, sequences):
        if sos_found:
            self.winner = self.current_player
            self.game_over = True

    def check_game_over(self):

        if not self.game_over and self.board.is_board_full():
            self.game_over = True
            self.winner = "Draw"

    def handle_turn_switch(self, sos_found):
        if not self.game_over:
            self.switch_turn()


"""General Game Mode: Most SOSs wins"""


class GeneralGame(SOSGame):
    """
    General game mode implementation
    - Players earn points for each SOS formed
    - Player gets another turn after forming SOS
    - Winner is player with most points when board is full
    """

    def __init__(self):
        super().__init__()
        self.game_mode = self.GENERAL_MODE

    def handle_sos_found(self, sos_found, sequences):
        """In General mode, award points for each SOS"""
        if sos_found:
            points = len(sequences)
            self.current_player.add_score(points)

    def check_game_over(self):
        if self.board.is_board_full():
            self.game_over = True
            # Determine winner by score
            if self.blue_player.score > self.red_player.score:
                self.winner = self.blue_player
            elif self.red_player.score > self.blue_player.score:
                self.winner = self.red_player
            else:
                self.winner = "Draw"

    def handle_turn_switch(self, sos_found):
        if not sos_found:
            self.switch_turn()


def create_game(mode):
    if mode == SOSGame.SIMPLE_MODE:
        return SimpleGame()
    elif mode == SOSGame.GENERAL_MODE:
        return GeneralGame()
    else:
        raise ValueError("Invalid game mode")