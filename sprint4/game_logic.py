"""
Hashim Abdulla
SOS Game Logic Module - Sprint 4 increment
Extended with Player class hierarchy for human and computer opponents
Includes computer AI with basic strategy
"""

import random


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
    """Base class for all player types"""

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

    def is_human(self):
        """Abstract method - subclasses must implement"""
        raise NotImplementedError("Subclasses must implement is_human()")


class HumanPlayer(Player):
    """Human player controlled through GUI interaction"""

    def __init__(self, name, color):
        super().__init__(name, color)

    def is_human(self):
        """Human players return True"""
        return True


class ComputerPlayer(Player):
    """Computer player with AI decision making"""

    def __init__(self, name, color, game):
        super().__init__(name, color)
        self.game = game  # Reference to game for board analysis

    def is_human(self):
        """Computer players return False"""
        return False

    def make_move(self):
        """
        AI decision-making: returns (row, col, letter) for next move
        Strategy priority:
        1. Find winning move (forms SOS)
        2. Find blocking move (prevents opponent win in Simple)
        3. Find scoring move (forms SOS in General)
        4. Make random valid move
        """
        # Priority 1: Look for winning/scoring moves
        winning_move = self.find_winning_move()
        if winning_move:
            return winning_move

        # Priority 2: Block opponent in Simple mode
        if self.game.game_mode == SOSGame.SIMPLE_MODE:
            blocking_move = self.find_blocking_move()
            if blocking_move:
                return blocking_move

        # Priority 3: In General mode, prefer scoring moves
        if self.game.game_mode == SOSGame.GENERAL_MODE:
            scoring_move = self.find_scoring_move()
            if scoring_move:
                return scoring_move

        # Priority 4: Random valid move
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None

        row, col = random.choice(valid_moves)
        letter = self.choose_letter()
        return (row, col, letter)

    def get_valid_moves(self):
        """Returns list of (row, col) tuples for all empty cells"""
        valid = []
        for row in range(self.game.board.size):
            for col in range(self.game.board.size):
                if self.game.board.is_cell_empty(row, col):
                    valid.append((row, col))
        return valid

    def choose_letter(self):
        """Randomly choose 'S' or 'O'"""
        return random.choice(['S', 'O'])

    def find_winning_move(self):
        """
        Find a move that forms SOS (wins in Simple, scores in General)
        Returns (row, col, letter) or None
        """
        for row, col in self.get_valid_moves():
            for letter in ['S', 'O']:
                if self.simulate_move(row, col, letter):
                    return (row, col, letter)
        return None

    def find_blocking_move(self):
        """
        In Simple mode, find and block opponent's winning move
        Returns (row, col, letter) or None
        """
        # Check if opponent could win on next turn
        opponent = self.game.red_player if self == self.game.blue_player else self.game.blue_player

        for row, col in self.get_valid_moves():
            for letter in ['S', 'O']:
                # Simulate opponent making this move
                original = self.game.board.grid[row][col]
                self.game.board.grid[row][col] = letter

                sequences = self.game.board.check_sos_at_position(row, col)

                # Restore board
                self.game.board.grid[row][col] = original

                if len(sequences) > 0:
                    # Opponent would win here, so block it
                    return (row, col, letter)
        return None

    def find_scoring_move(self):
        """
        In General mode, find moves that form SOS for scoring
        Same as find_winning_move but called separately for clarity
        """
        return self.find_winning_move()

    def simulate_move(self, row, col, letter):
        """
        Simulate placing letter at position without modifying board
        Returns True if move forms SOS, False otherwise
        """
        # Temporarily place letter
        original = self.game.board.grid[row][col]
        self.game.board.grid[row][col] = letter

        # Check for SOS
        sequences = self.game.board.check_sos_at_position(row, col)

        # Restore original state
        self.game.board.grid[row][col] = original

        return len(sequences) > 0


def create_player(player_type, name, color, game=None):
    """
    Factory function to create player instances
    player_type: "Human" or "Computer"
    name: Player name (e.g., "Blue", "Red")
    color: Player color ("blue" or "red")
    game: Reference to game (required for ComputerPlayer)
    """
    if player_type == "Human":
        return HumanPlayer(name, color)
    elif player_type == "Computer":
        if game is None:
            raise ValueError("Computer player requires game reference")
        return ComputerPlayer(name, color, game)
    else:
        raise ValueError(f"Invalid player type: {player_type}")


class SOSGame:
    """Base class for SOS game with Template Method pattern"""

    SIMPLE_MODE = "Simple"
    GENERAL_MODE = "General"

    def __init__(self):
        self.board = None
        self.board_size = 3
        self.blue_player = None  # Will be set by set_players()
        self.red_player = None   # Will be set by set_players()
        self.current_player = None
        self.game_started = False
        self.game_over = False
        self.winner = None  # Can be blue_player, red_player, or "Draw"

    def set_board_size(self, size):
        if not GameBoard.is_valid_size(size):
            raise ValueError("Board size must be between 3 and 10")
        self.board_size = size

    def set_players(self, blue_player, red_player):
        """Set player instances (Human or Computer)"""
        self.blue_player = blue_player
        self.red_player = red_player

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
        """
        Template Method for making a move Common flow
        """
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


    def __init__(self):
        super().__init__()
        self.game_mode = self.SIMPLE_MODE

    def handle_sos_found(self, sos_found, sequences):
        """In Simple mode, first SOS wins immediately"""
        if sos_found:
            self.winner = self.current_player
            self.game_over = True

    def check_game_over(self):
        """Check if board is full (draw condition)"""
        if not self.game_over and self.board.is_board_full():
            self.game_over = True
            self.winner = "Draw"

    def handle_turn_switch(self, sos_found):
        """Always switch turns in Simple mode"""
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
        """Game ends when the board is full, winner would be determined by score"""
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
        """Only switch if no SOSs were formed"""
        if not sos_found:
            self.switch_turn()


def create_game(mode):
    """Factory function to create game instances"""
    if mode == SOSGame.SIMPLE_MODE:
        return SimpleGame()
    elif mode == SOSGame.GENERAL_MODE:
        return GeneralGame()
    else:
        raise ValueError("Invalid game mode")