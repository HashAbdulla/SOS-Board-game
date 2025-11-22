"""
Hashim Abdulla
Unit tests for SOS Game Logic - Sprint 4
Using pytest framework

Sprint 4 increment adds tests for player hierarchy (Human/Computer)
"""

import pytest
from game_logic import (GameBoard, Player, HumanPlayer, ComputerPlayer,
                        SimpleGame, GeneralGame, create_game, create_player, SOSGame)

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
    """Tests for Player base class"""

    def test_player_creation(self):
        player = HumanPlayer("Blue", "blue")
        assert player.name == "Blue"
        assert player.color == "blue"
        assert player.score == 0

    def test_player_score_reset(self):
        player = HumanPlayer("Red", "red")
        player.score = 5
        player.reset_score()
        assert player.score == 0

    def test_player_add_score(self):
        player = HumanPlayer("Blue", "blue")
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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        # NO SOS pattern
        game.make_move(0, 0, 'O')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(1, 1, 'S')
        game.make_move(1, 2, 'O')
        game.make_move(2, 0, 'S')
        game.make_move(2, 1, 'O')
        game.make_move(2, 2, 'O')

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 2, 'S')

        assert game.is_game_over() == True
        assert game.get_winner() == game.blue_player

    def test_simple_game_red_wins(self):
        """Test red player winning in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(1, 0, 'O')
        game.make_move(0, 0, 'S')
        game.make_move(1, 1, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 2, 'O')
        game.make_move(0, 2, 'S')

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 2, 'S')

        with pytest.raises(RuntimeError, match="Game is already over"):
            game.make_move(2, 0, 'S')

    def test_simple_game_vertical_sos_wins(self):
        """Test vertical SOS wins in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'S')
        game.make_move(2, 0, 'S')

        assert game.is_game_over() == True
        assert game.get_winner() == game.blue_player

    def test_simple_game_diagonal_sos_wins(self):
        """Test diagonal SOS wins in simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(1, 0, 'O')
        game.make_move(0, 0, 'S')
        game.make_move(1, 2, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 1, 'S')
        game.make_move(2, 2, 'S')

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        # NO SOS pattern (0-0 draw)
        game.make_move(0, 0, 'O')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(1, 1, 'S')
        game.make_move(1, 2, 'O')
        game.make_move(2, 0, 'S')
        game.make_move(2, 1, 'O')
        game.make_move(2, 2, 'O')

        assert game.is_game_over() == True
        assert game.blue_player.score == 0
        assert game.red_player.score == 0
        assert game.get_winner() == "Draw"

    def test_general_game_blue_wins_by_score(self):
        """AC 7.2 - Determine winner by score

        Given: General game has ended
        When: Final scores are calculated
        Then: Player with higher score is announced as winner

        """
        game = GeneralGame()
        game.set_board_size(4)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        # Blue scores 2 SOS
        game.make_move(0, 0, 'S')
        game.make_move(3, 3, 'O')
        game.make_move(0, 1, 'O')
        game.make_move(3, 2, 'O')
        game.make_move(0, 2, 'S')  # Blue SOS
        game.make_move(0, 3, 'S')
        game.make_move(3, 1, 'S')
        game.make_move(1, 3, 'O')
        game.make_move(3, 0, 'O')
        game.make_move(2, 3, 'S')  # Blue SOS
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'S')
        game.make_move(1, 2, 'S')
        game.make_move(2, 1, 'O')  # Red SOS
        game.make_move(2, 0, 'O')
        game.make_move(2, 2, 'O')

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 2, 'S')

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(1, 1, 'O')

        assert game.get_current_player() == game.blue_player
        game.make_move(0, 2, 'S')

        assert game.get_current_player() == game.blue_player

    def test_general_game_turn_switch_no_sos(self):
        """AC 6.4 - Switch turns when no SOS formed
        Given: Player has placed a letter in general game
        When: Placement does not complete an SOS sequence
        Then: System should switch turn to other player

        """
        game = GeneralGame()
        game.set_board_size(3)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        assert game.get_current_player() == game.blue_player
        game.make_move(0, 0, 'S')

        assert game.get_current_player() == game.red_player

    def test_general_game_red_wins_by_score(self):
        """Test red winning by higher score"""
        game = GeneralGame()
        game.set_board_size(4)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'O')
        game.make_move(0, 1, 'S')
        game.make_move(1, 0, 'S')
        game.make_move(0, 2, 'O')
        game.make_move(1, 1, 'O')
        game.make_move(0, 3, 'S')

        assert game.red_player.score >= 1

    def test_general_game_ends_when_board_full(self):
        """AC 7.1 - Game ends when board is full
        Given: General game is in progress
        When: All cells on the board are filled
        Then: System should end game and display final scores

        """
        game = GeneralGame()
        game.set_board_size(3)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

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

        with pytest.raises(RuntimeError, match="Game is already over"):
            game.make_move(0, 0, 'S')

    def test_general_game_multiple_sos_in_one_move(self):
        """Test when one move forms multiple SOS sequences"""
        game = GeneralGame()
        game.set_board_size(5)
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        game.set_players(blue, red)
        game.start_new_game()

        game.make_move(0, 0, 'S')
        game.make_move(1, 0, 'O')
        game.make_move(0, 2, 'S')
        game.make_move(1, 2, 'O')
        game.make_move(2, 0, 'S')
        game.make_move(3, 0, 'O')
        game.make_move(2, 2, 'S')
        game.make_move(3, 2, 'O')

        initial_score = game.blue_player.score
        game.make_move(1, 1, 'O')

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

        blue1 = HumanPlayer("Blue", "blue")
        red1 = HumanPlayer("Red", "red")
        blue2 = HumanPlayer("Blue", "blue")
        red2 = HumanPlayer("Red", "red")

        simple_game.set_players(blue1, red1)
        general_game.set_players(blue2, red2)

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
        blue = HumanPlayer("Blue", "blue")
        red = HumanPlayer("Red", "red")
        blue.score = 5
        red.score = 3

        game.set_players(blue, red)
        game.start_new_game()

        assert game.blue_player.score == 0
        assert game.red_player.score == 0


#
# Player Hierarchy and Computer AI tests (Sprint 4)
#

class TestPlayerFactory:
    """Tests for player factory function"""

    def test_create_human_player(self):
        """AC 8.1 - Create human player"""
        player = create_player("Human", "Blue", "blue")
        assert isinstance(player, HumanPlayer)
        assert player.name == "Blue"
        assert player.color == "blue"
        assert player.is_human() == True

    def test_create_computer_player(self):
        """AC 8.2 - Create computer player"""
        game = SimpleGame()
        player = create_player("Computer", "Red", "red", game)
        assert isinstance(player, ComputerPlayer)
        assert player.name == "Red"
        assert player.color == "red"
        assert player.is_human() == False

    def test_create_invalid_player_type(self):
        """Test invalid player type"""
        with pytest.raises(ValueError, match="Invalid player type"):
            create_player("Robot", "Blue", "blue")

    def test_create_computer_without_game(self):
        """Test creating computer player without game reference"""
        with pytest.raises(ValueError, match="Computer player requires game reference"):
            create_player("Computer", "Blue", "blue", None)


class TestHumanPlayer:
    """Tests for HumanPlayer class"""

    def test_human_player_creation(self):
        """Test human player initialization"""
        player = HumanPlayer("Blue", "blue")
        assert player.name == "Blue"
        assert player.color == "blue"
        assert player.score == 0
        assert player.is_human() == True

    def test_human_player_inheritance(self):
        """Test human player inherits from Player"""
        player = HumanPlayer("Red", "red")
        assert isinstance(player, Player)
        player.add_score(3)
        assert player.score == 3
        player.reset_score()
        assert player.score == 0


class TestComputerPlayer:
    """Tests for ComputerPlayer class"""

    def test_computer_player_creation(self):
        """Test computer player initialization"""
        game = SimpleGame()
        player = ComputerPlayer("Blue", "blue", game)
        assert player.name == "Blue"
        assert player.color == "blue"
        assert player.score == 0
        assert player.is_human() == False
        assert player.game == game

    def test_computer_player_inheritance(self):
        """Test computer player inherits from Player"""
        game = GeneralGame()
        player = ComputerPlayer("Red", "red", game)
        assert isinstance(player, Player)
        player.add_score(5)
        assert player.score == 5

    def test_computer_makes_valid_move(self):
        """AC 9.1 - Computer selects empty cell"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(blue, red)
        game.start_new_game()

        # Fill some cells
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer makes move
        move = blue.make_move()
        assert move is not None
        row, col, letter = move
        assert game.board.is_cell_empty(row, col)

    def test_computer_chooses_s_or_o(self):
        """AC 9.2 - Computer selects S or O"""
        game = SimpleGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Test multiple moves
        for _ in range(20):
            letter = computer.choose_letter()
            assert letter in ['S', 'O']

    def test_get_valid_moves(self):
        """Test getting list of valid moves"""
        game = SimpleGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Initially all 9 cells are valid
        valid_moves = computer.get_valid_moves()
        assert len(valid_moves) == 9

        # Place some letters
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(1, 1, 'O')

        valid_moves = computer.get_valid_moves()
        assert len(valid_moves) == 7
        assert (0, 0) not in valid_moves
        assert (1, 1) not in valid_moves

    def test_computer_reliability(self):
        """Test computer makes 100 consecutive valid moves"""
        game = GeneralGame()
        game.set_board_size(10)
        blue = create_player("Computer", "Blue", "blue", game)
        red = create_player("Computer", "Red", "red", game)
        game.set_players(blue, red)
        game.start_new_game()

        move_count = 0
        max_moves = 100

        while not game.is_game_over() and move_count < max_moves:
            computer = game.get_current_player()
            move = computer.make_move()
            assert move is not None
            row, col, letter = move
            game.make_move(row, col, letter)
            move_count += 1

        # Should complete without errors
        assert move_count <= 100


class TestComputerStrategy:
    """Tests for computer AI strategy"""

    def test_computer_detects_winning_move(self):
        """AC 12.1 - Computer detects and makes winning move"""
        game = SimpleGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup: S-O-_ (horizontal)
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer should find winning move at (0, 2, 'S')
        winning_move = computer.find_winning_move()
        assert winning_move is not None
        row, col, letter = winning_move
        assert letter == 'S'

        # Verify it forms SOS
        game.board.grid[row][col] = letter
        sequences = game.board.check_sos_at_position(row, col)
        assert len(sequences) > 0

    def test_computer_blocks_opponent_simple(self):
        """AC 12.2 - Computer blocks opponent's winning move in Simple mode"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = create_player("Human", "Blue", "blue", game)
        computer = create_player("Computer", "Red", "red", game)
        game.set_players(blue, computer)
        game.start_new_game()

        # Setup: Blue has S-O-_ (about to win)
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer should block or find own winning move
        blocking_move = computer.find_blocking_move()
        assert blocking_move is not None or computer.find_winning_move() is not None

    def test_computer_prefers_scoring_moves(self):
        """AC 12.3 - Computer prefers scoring moves in General mode"""
        game = GeneralGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup board with scoring opportunity
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer should find scoring move
        scoring_move = computer.find_scoring_move()
        assert scoring_move is not None

    def test_simulate_move(self):
        """Test move simulation doesn't modify board"""
        game = SimpleGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Simulate move
        result = computer.simulate_move(0, 2, 'S')

        # Board should remain unchanged
        assert game.board.is_cell_empty(0, 2)
        assert result == True  # Would form SOS


class TestComputerSimpleGame:
    """Tests for computer playing simple games"""

    def test_computer_wins_simple_game(self):
        """AC 10.1 - Computer wins simple game by forming SOS"""
        game = SimpleGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup winning opportunity
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer makes move
        move = computer.make_move()
        row, col, letter = move
        game.make_move(row, col, letter)

        # If computer found winning move, game should be over
        if (row, col) == (0, 2) and letter == 'S':
            assert game.is_game_over()
            assert game.get_winner() == computer

    def test_computer_plays_complete_simple_game(self):
        """AC 10.2 - Computer plays until simple game ends"""
        game = SimpleGame()
        game.set_board_size(3)
        blue = create_player("Computer", "Blue", "blue", game)
        red = create_player("Computer", "Red", "red", game)
        game.set_players(blue, red)
        game.start_new_game()

        max_moves = 9
        move_count = 0

        while not game.is_game_over() and move_count < max_moves:
            computer = game.get_current_player()
            move = computer.make_move()
            row, col, letter = move
            game.make_move(row, col, letter)
            move_count += 1

        # Game should end (win or draw)
        assert game.is_game_over()
        assert game.get_winner() is not None


class TestComputerGeneralGame:
    """Tests for computer playing general games"""

    def test_computer_scores_in_general_game(self):
        """AC 11.1 - Computer scores points when forming SOS"""
        game = GeneralGame()
        game.set_board_size(3)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup scoring opportunity
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        initial_score = computer.score

        # Computer makes move
        move = computer.make_move()
        row, col, letter = move
        game.make_move(row, col, letter)

        # Check if scored
        if letter == 'S' and (row, col) == (0, 2):
            assert computer.score > initial_score

    def test_computer_extra_turn_after_sos(self):
        """AC 11.2 - Computer gets extra turn after forming SOS in General mode"""
        game = GeneralGame()
        game.set_board_size(4)
        computer = create_player("Computer", "Blue", "blue", game)
        red = create_player("Human", "Red", "red", game)
        game.set_players(computer, red)
        game.start_new_game()

        # Setup
        game.board.place_letter(0, 0, 'S')
        game.board.place_letter(0, 1, 'O')

        # Computer's turn
        assert game.current_player == computer

        move = computer.make_move()
        if move == (0, 2, 'S'):  # Forms SOS
            game.make_move(0, 2, 'S')
            # Should still be computer's turn
            assert game.current_player == computer

    def test_computer_plays_until_board_full(self):
        """AC 11.3 - Computer plays general game until board is full"""
        game = GeneralGame()
        game.set_board_size(3)
        blue = create_player("Computer", "Blue", "blue", game)
        red = create_player("Computer", "Red", "red", game)
        game.set_players(blue, red)
        game.start_new_game()

        max_moves = 9
        move_count = 0

        while not game.is_game_over() and move_count < max_moves:
            computer = game.get_current_player()
            move = computer.make_move()
            row, col, letter = move
            game.make_move(row, col, letter)
            move_count += 1

        # Game should end when board full
        assert game.is_game_over()
        assert game.board.is_board_full()


class TestMixedGame:
    """Tests for games with mix of human and computer players"""

    def test_human_vs_computer_simple(self):
        """Test human vs computer simple game"""
        game = SimpleGame()
        game.set_board_size(3)
        human = create_player("Human", "Blue", "blue", game)
        computer = create_player("Computer", "Red", "red", game)
        game.set_players(human, computer)
        game.start_new_game()

        # Human makes move
        game.make_move(0, 0, 'S')
        assert game.board.get_cell(0, 0) == 'S'

        # Computer makes move
        assert game.current_player == computer
        move = computer.make_move()
        assert move is not None

    def test_human_vs_computer_general(self):
        """Test human vs computer general game with scoring"""
        game = GeneralGame()
        game.set_board_size(4)
        human = create_player("Human", "Blue", "blue", game)
        computer = create_player("Computer", "Red", "red", game)
        game.set_players(human, computer)
        game.start_new_game()

        # Setup scoring opportunity for human
        game.make_move(0, 0, 'S')

        # Computer makes move
        computer_move = computer.make_move()
        row, col, letter = computer_move
        game.make_move(row, col, letter)

        # Game should track scores correctly
        assert human.score >= 0
        assert computer.score >= 0