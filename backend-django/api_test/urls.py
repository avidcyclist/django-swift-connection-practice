from django.urls import path
from .views import PlayerInfoView, WorkoutView, PlayerPhaseView

urlpatterns = [
    path('api/player-info/', PlayerInfoView.as_view(), name='player-info'),
    path('api/player-workout/', WorkoutView.as_view(), name='player-workout'),
    path('api/player-phases/<int:player_id>/', PlayerPhaseView.as_view(), name='player-phases'),
]