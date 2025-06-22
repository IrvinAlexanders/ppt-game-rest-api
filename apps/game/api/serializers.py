from rest_framework import serializers

from apps.game.models import Game, Player, Round
from apps.game.api.services import determine_round_winner, determine_game_winner


class ErrorDetailSerializer(serializers.Serializer):
    """Serializer for error details.
    """
    detail = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Error message detailing the issue"
    )
    code = serializers.CharField(
        max_length=50,
        required=True,
        help_text="Error code representing the type of error"
    )


class NewGameSerializer(serializers.Serializer):
    """Serializer for creating a new game.
    """
    player1_name = serializers.CharField(
        max_length=100,
        required=True,
        help_text="Name of the first player"
    )
    player2_name = serializers.CharField(
        max_length=100,
        required=True,
        help_text="Name of the second player"
    )

    def create(self, validated_data):
        """Create a new game instance."""
        if str(validated_data['player1_name']).lower() == str(validated_data['player2_name']).lower():
            raise serializers.ValidationError(
                ErrorDetailSerializer({
                    'detail': "Player names must be different.",
                    'code': 'duplicate_player_names'
                }).data
            )

        if Player.objects.filter(name=validated_data['player1_name']).exists():
            player1 = Player.objects.get(name=validated_data['player1_name'])
        else:
            player1 = Player.objects.create(name=validated_data['player1_name'])
        
        if Player.objects.filter(name=validated_data['player2_name']).exists():
            player2 = Player.objects.get(name=validated_data['player2_name'])
        else:
            player2 = Player.objects.create(name=validated_data['player2_name'])

        game = Game.objects.create(player1=player1, player2=player2)

        return game


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for the Player model."""
    class Meta:
        model = Player
        fields = ['id', 'name', 'score']
        read_only_fields = ['id']


class RoundSerializer(serializers.ModelSerializer):
    """Serializer for the Round model."""
    player1_choice = serializers.ChoiceField(choices=Round.GAME_CHOICES)
    player2_choice = serializers.ChoiceField(choices=Round.GAME_CHOICES)
    round_winner = PlayerSerializer(read_only=True)
    game = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Round
        fields = [
            'id',
            'round_number',
            'player1_choice',
            'player2_choice',
            'round_winner',
            'game',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 
            'round_winner', 
            'game', 
            'created_at', 
            'updated_at',
            'round_number'
        ]
    
    def create(self, validated_data):
        """Create a new round instance and determine the winner."""
        game = validated_data.get('game')
        if not game:
            raise serializers.ValidationError({

            })

        round_number = game.rounds.count() + 1
        round_obj = Round.objects.create(
            game=game,
            round_number=round_number,
            player1_choice=validated_data['player1_choice'],
            player2_choice=validated_data['player2_choice']
        )

        # Determine the winner of the round
        winner = determine_round_winner(round_obj)
        if winner:
            round_obj.round_winner = winner
            round_obj.save()

        # Check if the game has a winner after this round
        determine_game_winner(game)

        return round_obj


class GameSerializer(serializers.ModelSerializer):
    """Serializer for the Game model.
    """
    player1 = PlayerSerializer(read_only=True)
    player2 = PlayerSerializer(read_only=True)
    winner = PlayerSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    finished_at = serializers.DateTimeField(read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            'id',
            'player1',
            'player2',
            'winner',
            'created_at',
            'finished_at',
            'rounds'
            ]
        read_only_fields = ['id', 'created_at', 'finished_at', 'winner']
