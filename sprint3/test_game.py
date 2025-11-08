"""
Hashim Abdulla
Unit tests for SOS Game Logic - Sprint 3
Using pytest framework
"""

import pytest
from game_logic import GameBoard, Player, SimpleGame, GeneralGame, create_game, SOSGame


class TestGameBoard:
    """Tests for GameBoard class"""

    def test_valid_board_size_creation(self):
        """AC 1.1 - Valid board size selection"""
        board = GameBoard(5)
        assert board.size == 5
        assert len(board.grid) == 5
        assert len(board.grid[0]) == 5

    def test_invalid_board_size_too_small(self):
        """AC 1.2 - Invalid board size selection (too small)"""
        with pytest.raises(ValueError, match="Board size must be between 3 and 10"):
            GameBoard(2)

    def test_invalid_board_size_too_large(self):
        """AC 1.2 - Invalid board size selection (too large)"""
        with pytest.raises(ValueError, match="Board size must be between 3 and 10"):
            GameBoard(15)

    def test_board_initialized_empty(self):
        """AC 3.2 - Display empty board"""
        board = GameBoard(4)
        for row in board.grid:
            for cell in row:
                assert cell == ' '

    def test_is_cell_empty(self):
        board = GameBoard(3)
        assert board.is_cell_empty(0, 0) == True
        board.grid[0][0] = 'S'
        assert board.is_cell_empty(0, 0) == False

    def test_place_letter_valid(self):
        """AC 4.1 / 6.1 - Valid move placement"""
        board = GameBoard(3)
        board.place_letter(1, 1, 'S')
        assert board.get_cell(1, 1) == 'S'

        board.place_letter(0, 2, 'O')
        assert board.get_cell(0, 2) == 'O'

    def test_place_letter_on_occupied_cell(self):
        """AC 4.2 / 6.2 - Invalid move on occupied cell"""
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')

        with pytest.raises(ValueError, match="Cell is already occupied"):
            board.place_letter(0, 0, 'O')

    def test_place_invalid_letter(self):
        board = GameBoard(3)
        with pytest.raises(ValueError, match="Letter must be S or O"):
            board.place_letter(0, 0, 'X')

    def test_board_full_detection(self):
        board = GameBoard(3)
        assert board.is_board_full() == False

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

    def test_check_horizontal_sos(self):
        """Test detecting horizontal SOS"""
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')
        board.place_letter(0, 1, 'O')
        board.place_letter(0, 2, 'S')

        sequences = board.check_sos_at_position(0, 2)
        assert len(sequences) == 1
        assert sequences[0] == [(0, 0), (0, 1), (0, 2)]

    def test_check_vertical_sos(self):
        """Test detecting vertical SOS"""
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')
        board.place_letter(1, 0, 'O')
        board.place_letter(2, 0, 'S')

        sequences = board.check_sos_at_position(2, 0)
        assert len(sequences) == 1

    def test_check_diagonal_sos(self):
        """Test detecting diagonal SOS"""
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')
        board.place_letter(1, 1, 'O')
        board.place_letter(2, 2, 'S')

        sequences = board.check_sos_at_position(2, 2)
        assert len(sequences) == 1

    def test_no_sos_detected(self):
        """Test when no SOS is formed"""
        board = GameBoard(3)
        board.place_letter(0, 0, 'S')
        board.place_letter(0, 1, 'S')

        sequences = board.check_sos_at_position(0, 1)
        assert len(sequences) == 0


class TestPlayer:
    """Tests for Player class"""

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

    def test_player_add_score(self):
        player = Player("Blue", "blue")
        player.add_score(1)
        assert player.score == 1
        player.add_score(2)
        assert player.score == 3


class TestSimpleGame:
    """Tests for Simple Game mode"""

    def test_simple_game_draw(self):
        """AC 5.2 - Draw condition in simple game
        Given: Simple game is in progress
        When: Board is completely filled with no SOS sequence formed
        Then: System should display draw message
        """
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # VERIFIED SAFE PATTERN - NO SOS ANYWHERE
        # O O S
        # S S O
        # S O O
        game.make_move(0, 0, 'O')  # Blue
        game.make_move(0, 1, 'O')  # Red
        game.make_move(0, 2, 'S')  # Blue
        game.make_move(1, 0, 'S')  # Red
        game.make_move(1, 1, 'S')  # Blue
        game.make_move(1, 2, 'O')  # Red
        game.make_move(2, 0, 'S')  # Blue
        game.make_move(2, 1, 'O')  # Red
        game.make_move(2, 2, 'O')  # Blue

        assert game.is_game_over() == True
        assert game.get_winner() == "Draw"
        assert game.blue_player.score == 0
        assert game.red_player.score == 0

    def test_simple_game_creation(self):
        """Test creating a simple game"""
        game = SimpleGame()
        assert game.game_mode == SOSGame.SIMPLE_MODE

    def test_simple_game_blue_wins(self):
        """AC 5.1 - Win condition in simple game
        Given: Simple game is in progress
        When: Blue player forms an SOS sequence
        Then: System should display Blue as winner
        """
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # Blue makes SOS horizontally: S-O-S
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(1, 0, 'S')  # Red
        game.make_move(0, 1, 'O')  # Blue
        game.make_move(1, 1, 'O')  # Red
        game.make_move(0, 2, 'S')  # Blue - forms SOS!

        assert game.is_game_over() == True
        assert game.get_winner() == game.blue_player

    def test_simple_game_red_wins(self):
        """Test red player winning in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # Red makes SOS
        game.make_move(1, 0, 'O')  # Blue
        game.make_move(0, 0, 'S')  # Red
        game.make_move(1, 1, 'S')  # Blue
        game.make_move(0, 1, 'O')  # Red
        game.make_move(1, 2, 'O')  # Blue
        game.make_move(0, 2, 'S')  # Red - forms SOS!

        assert game.is_game_over() == True
        assert game.get_winner() == game.red_player



    def test_simple_game_prevents_moves_after_game_over(self):
        """AC 5.3 - Prevent moves after game ends
        Given: Simple game has ended
        When: Player attempts to make a move
        Then: System should not allow any further moves
        """
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # Blue wins
        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 2, 'S')  # Blue wins

        # Try to make another move
        with pytest.raises(RuntimeError, match="Game is already over"):
            game.make_move(2, 0, 'S')

    def test_simple_game_vertical_sos_wins(self):
        """Test vertical SOS wins in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # Blue makes vertical SOS
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(0, 1, 'O')  # Red
        game.make_move(1, 0, 'O')  # Blue
        game.make_move(1, 1, 'S')  # Red
        game.make_move(2, 0, 'S')  # Blue - vertical SOS!

        assert game.is_game_over() == True
        assert game.get_winner() == game.blue_player

    def test_simple_game_diagonal_sos_wins(self):
        """Test diagonal SOS wins in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        game.start_new_game()

        # Red makes diagonal SOS
        game.make_move(1, 0, 'O')  # Blue
        game.make_move(0, 0, 'S')  # Red
        game.make_move(1, 2, 'O')  # Blue
        game.make_move(1, 1, 'O')  # Red
        game.make_move(0, 1, 'S')  # Blue
        game.make_move(2, 2, 'S')  # Red - diagonal SOS! (0,0)-(1,1)-(2,2)

        assert game.is_game_over() == True
        assert game.get_winner() == game.red_player



class TestGeneralGame:
    """Tests for General Game mode"""

    def test_general_game_draw_same_score(self):
        """AC 7.3 - Draw condition in general game
        Given: General game has ended
        When: Both players have the same score
        Then: System should display draw message
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        # NO SOS ANYWHERE (0-0 draw)
        # O O S
        # S S O
        # S O O
        game.make_move(0, 0, 'O')  # Blue
        game.make_move(0, 1, 'O')  # Red
        game.make_move(0, 2, 'S')  # Blue
        game.make_move(1, 0, 'S')  # Red
        game.make_move(1, 1, 'S')  # Blue
        game.make_move(1, 2, 'O')  # Red
        game.make_move(2, 0, 'S')  # Blue
        game.make_move(2, 1, 'O')  # Red
        game.make_move(2, 2, 'O')  # Blue

        assert game.is_game_over() == True
        assert game.blue_player.score == 0
        assert game.red_player.score == 0
        assert game.get_winner() == "Draw"


    def test_general_game_blue_wins_by_score(self):
        """AC 7.2 - Determine winner by score (Blue wins with higher score)
        Given: General game has ended
        When: Final scores are calculated
        Then: Player with higher score is announced as winner
        """
        game = GeneralGame()
        game.set_board_size(4)
        game.start_new_game()

        # Blue scores 2 SOS, Red scores 1 SOS

        # Blue horizontal SOS at row 0: (0,0)S-(0,1)O-(0,2)S
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(3, 3, 'O')  # Red (far corner, safe)
        game.make_move(0, 1, 'O')  # Blue
        game.make_move(3, 2, 'O')  # Red (safe)
        game.make_move(0, 2, 'S')  # Blue - SOS! Blue=1, continues

        # Blue vertical SOS at column 3: (0,3)S-(1,3)O-(2,3)S
        game.make_move(0, 3, 'S')  # Blue continues
        game.make_move(3, 1, 'S')  # Red (safe)
        game.make_move(1, 3, 'O')  # Blue
        game.make_move(3, 0, 'O')  # Red (safe)
        game.make_move(2, 3, 'S')  # Blue - SOS! Blue=2, continues

        # Blue makes non-scoring move
        game.make_move(1, 0, 'O')  # Blue continues

        # Red horizontal SOS at row 3: (3,0)O-(3,1)S-(3,2)O is not SOS!
        # Let's make Red get 1 point with vertical: (1,1)S-(2,1)O-(3,1)S
        game.make_move(1, 1, 'S')  # Red
        game.make_move(1, 2, 'S')  # Blue
        game.make_move(2, 1, 'O')  # Red - completes vertical SOS! Red=1, continues

        # Fill remaining cells with no more SOS
        game.make_move(2, 0, 'O')  # Red continues
        game.make_move(2, 2, 'O')  # Blue

        assert game.is_game_over() == True
        assert game.blue_player.score == 2
        assert game.red_player.score == 1
        assert game.get_winner() == game.blue_player

    def test_general_game_creation(self):
        """Test creating a general game"""
        game = GeneralGame()
        assert game.game_mode == SOSGame.GENERAL_MODE

    def test_general_game_scoring(self):
        """AC 6.3 - Award points for SOS formation
        Given: Current player has placed a letter in general game
        When: Placement completes one or more SOS sequences
        Then: System should award one point per SOS to that player
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        # Blue forms SOS
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(1, 0, 'S')  # Red
        game.make_move(0, 1, 'O')  # Blue
        game.make_move(1, 1, 'O')  # Red
        game.make_move(0, 2, 'S')  # Blue - forms SOS, gets 1 point

        assert game.blue_player.score == 1
        assert game.red_player.score == 0

    def test_general_game_extra_turn_after_sos(self):
        """AC 6.3 - Player gets another turn after forming SOS
        Given: Player forms SOS in general game
        When: SOS is completed
        Then: Same player gets another turn
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        # Blue forms SOS
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(1, 0, 'S')  # Red
        game.make_move(0, 1, 'O')  # Blue
        game.make_move(1, 1, 'O')  # Red

        assert game.get_current_player() == game.blue_player
        game.make_move(0, 2, 'S')  # Blue - forms SOS

        # Blue should still have the turn
        assert game.get_current_player() == game.blue_player

    def test_general_game_turn_switch_no_sos(self):
        """AC 6.4 - Switch turns when no SOS formed
        Given: Player has placed a letter in general game
        When: Placement does not complete an SOS sequence
        Then: System should switch turn to other player
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        assert game.get_current_player() == game.blue_player
        game.make_move(0, 0, 'S')  # Blue - no SOS

        # Turn should switch to Red
        assert game.get_current_player() == game.red_player



    def test_general_game_red_wins_by_score(self):
        """Test red winning by higher score"""
        game = GeneralGame()
        game.set_board_size(4)
        game.start_new_game()

        # Setup where Red scores more
        game.make_move(0, 0, 'O')  # Blue
        game.make_move(0, 1, 'S')  # Red
        game.make_move(1, 0, 'S')  # Blue
        game.make_move(0, 2, 'O')  # Red
        game.make_move(1, 1, 'O')  # Blue
        game.make_move(0, 3, 'S')  # Red - SOS! Red=1

        # Verify Red scored
        assert game.red_player.score >= 1



    def test_general_game_ends_when_board_full(self):
        """AC 7.1 - Game ends when board is full
        Given: General game is in progress
        When: All cells on the board are filled
        Then: System should end game and display final scores
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        # Fill the board with safe pattern
        # S S O
        # O O S
        # S S O
        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'S')
        game.make_move(0, 2, 'O')
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(1, 2, 'S')
        game.make_move(2, 0, 'S')
        game.make_move(2, 1, 'S')
        game.make_move(2, 2, 'O')

        assert game.board.is_board_full() == True
        assert game.is_game_over() == True

    def test_general_game_prevents_moves_after_over(self):
        """AC 7.4 - Prevent moves after game ends
        Given: General game has ended
        When: Player attempts to make a move
        Then: System should not allow any further moves
        """
        game = GeneralGame()
        game.set_board_size(3)
        game.start_new_game()

        # Fill board (safe pattern)
        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'S')
        game.make_move(0, 2, 'O')
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(1, 2, 'S')
        game.make_move(2, 0, 'S')
        game.make_move(2, 1, 'S')
        game.make_move(2, 2, 'O')

        assert game.is_game_over() == True

        # Try to make move after game over
        with pytest.raises(RuntimeError, match="Game is already over"):
            game.make_move(0, 0, 'S')

    def test_general_game_multiple_sos_in_one_move(self):
        """Test when one move forms multiple SOS sequences"""
        game = GeneralGame()
        game.set_board_size(5)
        game.start_new_game()

        # Setup board where placing 'O' in center forms multiple SOS
        game.make_move(0, 0, 'S')  # Blue
        game.make_move(1, 0, 'O')  # Red
        game.make_move(0, 2, 'S')  # Blue
        game.make_move(1, 2, 'O')  # Red
        game.make_move(2, 0, 'S')  # Blue
        game.make_move(3, 0, 'O')  # Red
        game.make_move(2, 2, 'S')  # Blue
        game.make_move(3, 2, 'O')  # Red

        # Now Blue places 'O' at (1,1) which could form multiple SOS
        # (0,0)S - (1,1)O - (2,2)S
        # (0,2)S - (1,1)O - (2,0)S
        initial_score = game.blue_player.score
        game.make_move(1, 1, 'O')  # Blue

        # Blue should score for any SOS sequences formed
        assert game.blue_player.score > initial_score
        assert game.blue_player.score == initial_score + 2


class TestGameFactory:
    """Tests for game factory method"""

    def test_create_simple_game(self):
        """Test factory creates SimpleGame"""
        game = create_game(SOSGame.SIMPLE_MODE)
        assert isinstance(game, SimpleGame)
        assert game.game_mode == SOSGame.SIMPLE_MODE

    def test_create_general_game(self):
        """Test factory creates GeneralGame"""
        game = create_game(SOSGame.GENERAL_MODE)
        assert isinstance(game, GeneralGame)
        assert game.game_mode == SOSGame.GENERAL_MODE



    def test_create_invalid_game(self):
        """Test factory with invalid mode"""
        with pytest.raises(ValueError, match="Invalid game mode"):
            create_game("InvalidMode")


class TestCommonGameLogic:
    """Tests for common game logic in base class"""

    def test_set_valid_board_size(self):
        """AC 1.1 - Valid board size in both modes"""
        simple_game = SimpleGame()
        general_game = GeneralGame()

        simple_game.set_board_size(7)
        general_game.set_board_size(8)

        assert simple_game.board_size == 7
        assert general_game.board_size == 8

    def test_set_invalid_board_size(self):
        """AC 1.2 - Invalid board size rejected in both modes"""
        simple_game = SimpleGame()

        with pytest.raises(ValueError):
            simple_game.set_board_size(1)
        with pytest.raises(ValueError):
            simple_game.set_board_size(20)

    def test_initial_turn_is_blue(self):
        """AC 3.3 - Blue player starts in both modes"""
        simple_game = SimpleGame()
        general_game = GeneralGame()

        simple_game.start_new_game()
        general_game.start_new_game()

        assert simple_game.get_current_player().color == "blue"
        assert general_game.get_current_player().color == "blue"

    def test_make_move_before_game_starts(self):
        """Test making move before starting game"""
        game = SimpleGame()

        with pytest.raises(RuntimeError, match="Game has not been started"):
            game.make_move(0, 0, 'S')

    def test_players_score_reset_on_new_game(self):
        """Test scores reset when new game starts"""
        game = GeneralGame()
        game.blue_player.score = 5
        game.red_player.score = 3

        game.start_new_game()

        assert game.blue_player.score == 0
        assert game.red_player.score == 0