from django.db import models

import uuid


class Player(models.Model):
    """Model representing a player in the game."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Score: {self.score})"
    

class Game(models.Model):
    """Model representing a game between two players."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player1 = models.ForeignKey(Player, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(
        Player, 
        related_name='winner', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.id} between {self.player1.name} and {self.player2.name}"


class Round(models.Model):
    """Model representing a round in a game."""
    GAME_CHOICES = [
        ('rock', 'Rock'),
        ('paper', 'Paper'),
        ('scissors', 'Scissors'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    round_number = models.IntegerField()
    player1_choice = models.CharField(max_length=10, choices=GAME_CHOICES)
    player2_choice = models.CharField(max_length=10, choices=GAME_CHOICES)
    round_winner = models.ForeignKey(
        Player,
        related_name='round_winner',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        related_name='rounds',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Round {self.round_number} of Game {self.game.id} - {self.player1_choice} vs {self.player2_choice}"
