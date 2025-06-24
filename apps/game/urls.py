from django.urls import path

from apps.game.api.views import (
    NewGameView,
    GameDetailView,
    NewRoundView,
    GameListView
)


urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('new/', NewGameView.as_view(), name='new_game'),
    path('<str:game_id>/', GameDetailView.as_view(), name='game_detail'),
    path('<str:game_id>/rounds/new/', NewRoundView.as_view(), name='new_round'),
]