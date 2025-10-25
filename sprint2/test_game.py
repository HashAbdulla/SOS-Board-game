"""
Unit tests for SOS Game Logic
Using pytest framework (my chosen xunit framework)

"""

import pytest
from game_logic import GameBoard, Player, SOSGame


class TestGameBoard:

    def test_valid_board_size_creation(self):
        """AC 1.1 - Valid board size selection
        Given: Player is on start screen
        When: Player selects valid board size (3-10)
        Then: The system should update the game to use the selected board size
        """
        board = GameBoard(5)
        assert board.size == 5
        assert len(board.grid) == 5
        assert len(board.grid[0]) == 5

    def test_invalid_board_size_too_small(self):
        """AC 1.2 - Invalid board size selection (too small)
        Given: Player is on start screen
        When: Player enters size less than 3
        Then: System should raise ValueError
        """
        with pytest.raises(ValueError, match="Board size must be between 3 and 10"):
            GameBoard(2)

    def test_invalid_board_size_too_large(self):
        """AC 1.2 - Invalid board size selection (too large)
        Given: Player is on start screen
        When: Player enters size greater than 10
        Then: System should raise ValueError
        """
        with pytest.raises(ValueError, match="Board size must be between 3 and 10"):
            GameBoard(15)

    def test_board_initialized_empty(self):
        """AC 3.2 - Display empty board
        Given: New game has been started
        When: Board is displayed
        Then: All cells should be empty
        """
        board = GameBoard(4)
        for row in board.grid:
            for cell in row:
                assert cell == ' '

    def test_is_cell_empty(self):
        """Test checking if cell is empty"""
        board = GameBoard(3)
        assert board.is_cell_empty(0, 0) == True
        board.grid[0][0] = 'S'
        assert board.is_cell_empty(0, 0) == False

    def test_place_letter_valid(self):
        """AC 4.1 / 6.1 - Valid move placement
        Given: It is current player's turn
        When: Player selects S or O and clicks empty cell
        Then: System should place the letter in that cell
        """
        board = GameBoard(3)
        board.place_letter(1, 1, 'S')
        assert board.get_cell(1, 1) == 'S'

        board.place_letter(0, 2, 'O')
        assert board.get_cell(0, 2) == 'O'

    def test_place_letter_on_occupied_cell(self):
        """AC 4.2 / 6.2 - Invalid move on occupied cell
        Given: It is current player's turn
        When: Player attempts to place letter in occupied cell
        Then: System should reject the move
        """
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')

        with pytest.raises(ValueError, match="Cell is already occupied"):
            board.place_letter(0, 0, 'O')

    def test_place_invalid_letter(self):
        board = GameBoard(3)
        with pytest.raises(ValueError, match="Letter must be S or O"):
            board.place_letter(0, 0, 'X')

    def test_board_full_detection(self):
        """Test detecting when board is full"""
        board = GameBoard(3)
        assert board.is_board_full() == False

        # Fill the board
        for i in range(3):
            for j in range(3):
                board.place_letter(i, j, 'S' if (i + j) % 2 == 0 else 'O')

        assert board.is_board_full() == True

    def test_board_reset(self):
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')
        board.place_letter(1, 1, 'O')

        board.reset()

        for row in board.grid:
            for cell in row:
                assert cell == ' '


class TestPlayer:

    def test_player_creation(self):
        player = Player("Blue", "blue")
        assert player.name == "Blue"
        assert player.color == "blue"
        assert player.score == 0

    def test_player_score_reset(self):
        player = Player("Red", "red")
        player.score = 5
        player.reset_score()
        assert player.score == 0


class TestSOSGame:

    def test_set_valid_board_size(self):
        """AC 1.1 - Valid board size selection in game logic"""
        game = SOSGame()
        game.set_board_size(7)
        assert game.board_size == 7

    def test_set_invalid_board_size(self):
        """AC 1.2 - Invalid board size selection in game logic"""
        game = SOSGame()
        with pytest.raises(ValueError):
            game.set_board_size(1)
        with pytest.raises(ValueError):
            game.set_board_size(20)

    def test_set_simple_game_mode(self):
        """AC 2.1 - Simple mode selection
        Given: Player has chosen valid board size
        When: Player selects "Simple Game" mode
        Then: System should start new SOS game in Simple mode
        """
        game = SOSGame()
        game.set_game_mode(SOSGame.SIMPLE_MODE)
        assert game.game_mode == SOSGame.SIMPLE_MODE

    def test_set_general_game_mode(self):
        """AC 2.2 - General mode selection
        Given: Player has chosen valid board size
        When: Player selects "General Game" mode
        Then: System should start new SOS game in General mode
        """
        game = SOSGame()
        game.set_game_mode(SOSGame.GENERAL_MODE)
        assert game.game_mode == SOSGame.GENERAL_MODE

    def test_set_invalid_game_mode(self):
        """Test setting invalid game mode"""
        game = SOSGame()
        with pytest.raises(ValueError):
            game.set_game_mode("Invalid")

    def test_start_new_game(self):
        """AC 3.1 - Start new game with valid selections
        Given: Player has selected valid board size and game mode
        When: Player clicks "New Game" button
        Then: System should initialize new game board with specified size and mode
        """
        game = SOSGame()
        game.set_board_size(5)
        game.set_game_mode(SOSGame.SIMPLE_MODE)
        game.start_new_game()

        assert game.board is not None
        assert game.board.size == 5
        assert game.game_started == True

    def test_initial_turn_is_blue(self):
        """AC 3.3 - Set initial turn
        Given: New game has been started
        When: Game begins
        Then: System should display which player has current turn (blue or red)
        Blue player should start first
        """
        game = SOSGame()
        game.start_new_game()
        assert game.get_current_player().color == "blue"

    def test_make_valid_move(self):
        """AC 4.1 - Valid move placement and turn switch
        Given: It is current player's turn in a simple game
        When: Player selects S or O and clicks empty cell
        Then: System should place the selected letter in that cell and switch turns
        """
        game = SOSGame()
        game.start_new_game()

        initial_player = game.get_current_player()
        game.make_move(0, 0, 'S')

        # Check letter was placed
        assert game.board.get_cell(0, 0) == 'S'

        # Check turn switched
        assert game.get_current_player() != initial_player

    def test_make_move_on_occupied_cell(self):
        """AC 4.2 - Invalid move on occupied cell"""
        game = SOSGame()
        game.start_new_game()
        game.make_move(0, 0, 'S')

        with pytest.raises(ValueError, match="Cell is already occupied"):
            game.make_move(0, 0, 'O')

    def test_make_move_before_game_starts(self):
        """Test making move before game is started"""
        game = SOSGame()
        with pytest.raises(RuntimeError, match="Game has not been started"):
            game.make_move(0, 0, 'S')

    def test_turn_switching(self):
        """Test that turns alternate between players"""
        game = SOSGame()
        game.start_new_game()

        assert game.get_current_player().color == "blue"
        game.make_move(0, 0, 'S')

        assert game.get_current_player().color == "red"
        game.make_move(0, 1, 'O')

        assert game.get_current_player().color == "blue"

    def test_players_score_reset_on_new_game(self):
        """Test that player scores reset when new game starts"""
        game = SOSGame()
        game.blue_player.score = 3
        game.red_player.score = 5

        game.start_new_game()

        assert game.blue_player.score == 0
        assert game.red_player.score == 0