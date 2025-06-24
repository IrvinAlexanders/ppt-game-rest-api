from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.http import HttpRequest
from drf_spectacular.utils import extend_schema

from apps.game.models import Game, Player, Round
from apps.game.api.serializers import (
    NewGameSerializer,
    GameSerializer,
    ErrorDetailSerializer,
    RoundSerializer
)


class NewGameView(APIView):
    """API view to create a new game.
    """
    permission_classes = [AllowAny]
    serializer_class = NewGameSerializer

    @extend_schema(
        summary="Create a new game",
        description="This endpoint allows you to create a new game by providing the names of two players.",
        request=NewGameSerializer,
        responses={
            201: GameSerializer,
            400: ErrorDetailSerializer
        }
    )
    def post(self, request):
        """Handle POST request to create a new game.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            return Response(
                GameSerializer(game).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GameDetailView(APIView):
    """API view to retrieve game details.
    """
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    @extend_schema(
        summary="Get game details",
        description="This endpoint allows you to retrieve the details of a specific game by its ID.",
        responses={
            200: GameSerializer,
            404: ErrorDetailSerializer
        }
    )
    def get(self, request: HttpRequest, game_id: str):
        """Handle GET request to retrieve game details.
        """
        try:
            game = Game.objects.get(id=game_id)
            return Response(self.serializer_class(game).data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(
                ErrorDetailSerializer(
                    {
                        "detail": "Game not found",
                        "code": "game_not_found"
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND
            )


class NewRoundView(APIView):
    """API view to create a new round in a game.
    """
    permission_classes = [AllowAny]
    serializer_class = RoundSerializer

    @extend_schema(
        summary="Create a new round",
        description="This endpoint allows you to create a new round in an existing game.",
        request=RoundSerializer,
        responses={
            201: RoundSerializer,
            400: "Bad Request",
            404: "Game not found"
        }
    )
    def post(self, request: HttpRequest, game_id: str):
        """Handle POST request to create a new round.
        """
        try:
            game = Game.objects.get(id=game_id)
            if game.finished_at or game.winner:
                return Response(
                    ErrorDetailSerializer(
                        {
                            "detail": "Cannot create a new round for a finished game",
                            "code": "game_finished"
                        }
                    ).data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(game=game)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(
                ErrorDetailSerializer(
                    {
                        "detail": "Game not found",
                        "code": "game_not_found"
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND
            )


class GameListView(APIView):
    """API view to list all games.
    """
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    @extend_schema(
        summary="List all games",
        description="This endpoint allows you to retrieve a list of all games.",
        responses={
            200: GameSerializer(many=True)
        }
    )
    def get(self, request: HttpRequest):
        """Handle GET request to list all games.
        """
        games = Game.objects.all()
        return Response(
            self.serializer_class(games, many=True).data,
            status=status.HTTP_200_OK
        )
