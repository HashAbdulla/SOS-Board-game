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


class Player:
    """Represents a player in the game"""

    def __init__(self, name, color):
        """Initialize player WITH name and color for better clarity"""
        self.name = name
        self.color = color  # 'blue' or 'red'
        self.score = 0

    def reset_score(self):
        self.score = 0

"""The main game logic"""
class SOSGame:

    SIMPLE_MODE = "Simple"
    GENERAL_MODE = "General"

    def __init__(self):
        self.board = None
        self.game_mode = self.SIMPLE_MODE
        self.board_size = 3
        self.blue_player = Player("Blue", "blue")
        self.red_player = Player("Red", "red")
        self.current_player = self.blue_player
        self.game_started = False

    def set_board_size(self, size):
        if not GameBoard.is_valid_size(size):
            raise ValueError("Board size must be between 3 and 10")
        self.board_size = size

    def set_game_mode(self, mode):
        if mode not in [self.SIMPLE_MODE, self.GENERAL_MODE]:
            raise ValueError("Mode must be Simple or General")
        self.game_mode = mode

    def start_new_game(self):
        self.board = GameBoard(self.board_size)
        self.current_player = self.blue_player
        self.blue_player.reset_score()
        self.red_player.reset_score()
        self.game_started = True

    def make_move(self, row, col, letter):
        if not self.game_started:
            raise RuntimeError("Game has not been started")

        if not self.board.is_cell_empty(row, col):
            raise ValueError("Cell is already occupied")

        self.board.place_letter(row, col, letter)
        self.switch_turn()

    def switch_turn(self):
        if self.current_player == self.blue_player:
            self.current_player = self.red_player
        else:
            self.current_player = self.blue_player

    def get_current_player(self):
        """Get the current player"""
        return self.current_player

    def get_board(self):
        """Get the game board"""
        return self.board
