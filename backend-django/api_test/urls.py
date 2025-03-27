from django.urls import path
from .views import PlayerInfoView, WorkoutView, PlayerPhaseView, save_workout_log, get_workout_logs, get_players

urlpatterns = [
    path('api/player-info/', PlayerInfoView.as_view(), name='player-info'),
    path('api/player-workout/', WorkoutView.as_view(), name='player-workout'),
    path('api/player-phases/<int:player_id>/', PlayerPhaseView.as_view(), name='player-phases'),
    path('api/save-workout-log/', save_workout_log, name='save-workout-log'),
    path('api/get-workout-logs/<int:player_id>/', get_workout_logs, name='get-workout-logs'),
    path('api/players/', get_players, name='get_players'),
]