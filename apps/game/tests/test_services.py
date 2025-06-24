from apps.game.tests.base import GameAPITestCase
from apps.game.models import Game, Player, Round
from apps.game.api.services import determine_game_winner, determine_round_winner


class GameServiceTestCase(GameAPITestCase):
    """Test case for game service functions."""

    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player1=self.player1, player2=self.player2)

    def test_determine_game_winner_null(self):
        """Should return None if no player has won 3 rounds."""
        # No rounds played
        winner = determine_game_winner(self.game)
        self.assertIsNone(winner)

    def test_determine_game_winner_player1(self):
        """Player 1 should win after 3 victories."""
        for i in range(1, 4):
            Round.objects.create(
                game=self.game,
                round_number=i,
                player1_choice='rock',
                player2_choice='scissors',
                round_winner=self.player1
            )
        winner = determine_game_winner(self.game)
        self.assertEqual(winner, self.player1)

    def test_determine_game_winner_player2(self):
        """Player 2 should win after 3 victories."""
        for i in range(1, 4):
            Round.objects.create(
                game=self.game,
                round_number=i,
                player1_choice='scissors',
                player2_choice='rock',
                round_winner=self.player2
            )
        winner = determine_game_winner(self.game)
        self.assertEqual(winner, self.player2)

    def test_determine_game_winner_no_winner_yet(self):
        """Should return None if neither player has 3 wins."""
        Round.objects.create(
            game=self.game,
            round_number=1,
            player1_choice='rock',
            player2_choice='scissors',
            round_winner=self.player1
        )
        Round.objects.create(
            game=self.game,
            round_number=2,
            player1_choice='scissors',
            player2_choice='rock',
            round_winner=self.player2
        )
        winner = determine_game_winner(self.game)
        self.assertIsNone(winner)

    def test_determine_round_winner_player1_wins(self):
        """Player 1 should win when their choice beats player 2."""
        round_ = Round.objects.create(
            game=self.game,
            round_number=1,
            player1_choice='rock',
            player2_choice='scissors'
        )
        winner = determine_round_winner(round_)
        self.assertEqual(winner, self.player1)

    def test_determine_round_winner_player2_wins(self):
        """Player 2 should win when their choice beats player 1."""
        round_ = Round.objects.create(
            game=self.game,
            round_number=2,
            player1_choice='scissors',
            player2_choice='rock'
        )
        winner = determine_round_winner(round_)
        self.assertEqual(winner, self.player2)

    def test_determine_round_winner_draw(self):
        """Should return None when both players choose the same."""
        round_ = Round.objects.create(
            game=self.game,
            round_number=3,
            player1_choice='rock',
            player2_choice='rock'
        )
        winner = determine_round_winner(round_)
        self.assertIsNone(winner)