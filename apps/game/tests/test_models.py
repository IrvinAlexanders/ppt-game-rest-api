from apps.game.tests.base import GameAPITestCase
from apps.game.models import Game, Player, Round


class GameModelTestCase(GameAPITestCase):
    """Test case for the Game model."""

    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player1=self.player1, player2=self.player2)

    def test_game_creation(self):
        """Test that a game can be created successfully."""
        self.assertIsInstance(self.game, Game)
        self.assertEqual(self.game.player1, self.player1)
        self.assertEqual(self.game.player2, self.player2)

    def test_game_str_method(self):
        """Test the string representation of the game."""
        expected_str = f"Game {self.game.id} between {self.player1.name} and {self.player2.name}"
        self.assertEqual(str(self.game), expected_str)


class PlayerModelTestCase(GameAPITestCase):
    """Test case for the Player model."""

    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.player = Player.objects.create(name="Test Player")

    def test_player_creation(self):
        """Test that a player can be created successfully."""
        self.assertIsInstance(self.player, Player)
        self.assertEqual(self.player.name, "Test Player")

    def test_player_str_method(self):
        """Test the string representation of the player."""
        self.assertEqual(str(self.player), "Test Player (Score: 0)")


class RoundModelTestCase(GameAPITestCase):
    """Test case for the Round model."""

    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player1=self.player1, player2=self.player2)
        self.round = Round.objects.create(game=self.game, round_number=1, round_winner=self.player1)

    def test_round_creation(self):
        """Test that a round can be created successfully."""
        self.assertIsInstance(self.round, Round)
        self.assertEqual(self.round.game, self.game)
        self.assertEqual(self.round.round_winner, self.player1)

    def test_round_str_method(self):
        """Test the string representation of the round."""
        expected_str = f"Round {self.round.round_number} of Game {self.round.game.id} - {self.round.player1_choice} vs {self.round.player2_choice}"
        self.assertEqual(str(self.round), expected_str)