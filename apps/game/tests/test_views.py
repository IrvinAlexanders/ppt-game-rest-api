from apps.game.tests.base import GameAPITestCase
from apps.game.models import Game, Player, Round

from django.urls import reverse
from rest_framework import status


class TestNewGameView(GameAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = "/api/game/new/"

    def test_create_new_game_success(self):
        data = {
            "player1_name": "Alice",
            "player2_name": "Bob"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["player1"]["name"] == "Alice"
        assert response.data["player2"]["name"] == "Bob"

    def test_create_new_game_missing_player1(self):
        data = {
            "player2_name": "Bob"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "player1_name" in response.data

    def test_create_new_game_missing_player2(self):
        data = {
            "player1_name": "Alice"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "player2_name" in response.data

    def test_create_new_game_empty_names(self):
        data = {
            "player1_name": "",
            "player2_name": ""
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "player1_name" in response.data
        assert "player2_name" in response.data

    def test_create_new_game_extra_fields_ignored(self):
        data = {
            "player1_name": "Alice",
            "player2_name": "Bob",
            "extra_field": "should be ignored"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data


class TestGameDetailView(GameAPITestCase):
    def setUp(self):
        super().setUp()
        self.player1 = Player.objects.create(name="Alice")
        self.player2 = Player.objects.create(name="Bob")
        self.game = Game.objects.create(player1=self.player1, player2=self.player2)
        self.url = "/api/game/{}/".format(self.game.id)

    def test_get_game_detail_success(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(self.game.id)
        assert response.data["player1"]["name"] == "Alice"
        assert response.data["player2"]["name"] == "Bob"

    def test_get_game_detail_not_found(self):
        invalid_url = "/api/game/00000000-0000-0000-0000-000000000000/"
        response = self.client.get(invalid_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Game not found"
        assert response.data["code"] == "game_not_found"


class TestNewRoundView(GameAPITestCase):
    def setUp(self):
        super().setUp()
        self.player1 = Player.objects.create(name="Alice")
        self.player2 = Player.objects.create(name="Bob")
        self.game = Game.objects.create(player1=self.player1, player2=self.player2)
        self.url = f"/api/game/{self.game.id}/rounds/new/"

    def test_create_new_round_success(self):
        data = {
            "player1_choice": "rock",
            "player2_choice": "scissors"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["player1_choice"] == "rock"
        assert response.data["player2_choice"] == "scissors"

    def test_create_new_round_invalid_choices(self):
        data = {
            "player1_choice": "invalid",
            "player2_choice": "scissors"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "player1_choice" in response.data

    def test_create_new_round_missing_fields(self):
        data = {
            "player1_choice": "rock"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "player2_choice" in response.data

    def test_create_new_round_game_not_found(self):
        url = "/api/game/00000000-0000-0000-0000-000000000000/rounds/new/"
        data = {
            "player1_choice": "rock",
            "player2_choice": "scissors"
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Game not found"
        assert response.data["code"] == "game_not_found"

    def test_create_new_round_game_already_finished(self):
        self.game.finished_at = "2024-01-01T00:00:00Z"
        self.game.save()
        data = {
            "player1_choice": "rock",
            "player2_choice": "scissors"
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Cannot create a new round for a finished game"
        assert response.data["code"] == "game_finished"


class TestGameListView(GameAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = "/api/game/"

    def test_list_games_empty(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 0

    def test_list_games_single(self):
        player1 = Player.objects.create(name="Alice")
        player2 = Player.objects.create(name="Bob")
        game = Game.objects.create(player1=player1, player2=player2)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(game.id)
        assert response.data[0]["player1"]["name"] == "Alice"
        assert response.data[0]["player2"]["name"] == "Bob"

    def test_list_games_multiple(self):
        player1 = Player.objects.create(name="Alice")
        player2 = Player.objects.create(name="Bob")
        player3 = Player.objects.create(name="Charlie")
        game1 = Game.objects.create(player1=player1, player2=player2)
        game2 = Game.objects.create(player1=player2, player2=player3)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        ids = [g["id"] for g in response.data]
        assert str(game1.id) in ids
        assert str(game2.id) in ids

    def test_list_games_fields(self):
        player1 = Player.objects.create(name="Alice")
        player2 = Player.objects.create(name="Bob")
        _ = Game.objects.create(player1=player1, player2=player2)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        game_data = response.data[0]
        # Check for expected fields in the response
        assert "id" in game_data
        assert "player1" in game_data
        assert "player2" in game_data
        assert "created_at" in game_data
