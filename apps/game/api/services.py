from django.utils import timezone

from apps.game.models import Round, Game, Player


CHOICES = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock',
}

def determine_round_winner(round_obj: Round) -> Player | None:
    """Determine the winner of a round based on player choices.
    If both players choose the same option, the round is a draw.
    If player1's choice beats player2's choice, player1 wins.
    If player2's choice beats player1's choice, player2 wins.

    Args:
        round_obj (Round): The round object containing player choices.
    Returns:
        Player | None: The winning player if a winner is determined, otherwise None.
    """
    p1 = round_obj.player1_choice
    p2 = round_obj.player2_choice

    if p1 == p2:
        round_obj.round_winner = None
    elif CHOICES.get(p1) == p2:
        round_obj.round_winner = round_obj.game.player1
    else:
        round_obj.round_winner = round_obj.game.player2

    round_obj.save()
    return round_obj.round_winner


def determine_game_winner(game_obj: Game) -> Player | None:
    """Determine the winner of a game based on the rounds played.
    A player wins the game if they win 3 rounds.
    If both players have not won 3 rounds, the game continues.
    Args:
        game_obj (Game): The game object containing player information and rounds.
    Returns:
        Player | None: The winning player if a winner is determined, otherwise None.
    """
    if not game_obj.rounds.exists():
        return None
    p1_wins = game_obj.rounds.filter(round_winner=game_obj.player1).count()
    p2_wins = game_obj.rounds.filter(round_winner=game_obj.player2).count()

    if p1_wins >= 3:
        game_obj.winner = game_obj.player1
        game_obj.finished_at = timezone.now()
        game_obj.save()
        return game_obj.player1
    elif p2_wins >= 3:
        game_obj.winner = game_obj.player2
        game_obj.finished_at = timezone.now()
        game_obj.save()
        return game_obj.player2

    return None