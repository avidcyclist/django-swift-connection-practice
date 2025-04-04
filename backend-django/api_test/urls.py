from django.urls import path
from .views import PlayerInfoView, WorkoutView, PlayerPhaseView, PlayerWarmupView, GetWorkoutLogView, save_workout_log, get_workout_logs, get_phase_workouts_by_week, get_players, get_player_id, get_player_correctives, get_phase_workouts_by_day

urlpatterns = [
    path('api/player-info/<int:player_id>/', PlayerInfoView.as_view(), name='player-info'),
    path('api/player-workout/', WorkoutView.as_view(), name='player-workout'),
    path('api/player-phases/<int:player_id>/', PlayerPhaseView.as_view(), name='player-phases'),
    path('api/save-workout-log/', save_workout_log, name='save-workout-log'),
    path('api/get-workout-logs/<int:player_id>/', get_workout_logs, name='get-workout-logs'),
    path('api/players/', get_players, name='get_players'),
    path('api/player-id/', get_player_id, name='get-player-id'),
    path('api/player/<int:player_id>/correctives/', get_player_correctives, name='get-player-correctives'),
    path('api/player-phases/<int:player_id>/workouts-by-day/', get_phase_workouts_by_day, name='workouts-by-day'),
    path('api/player-phases/<int:player_id>/workouts-by-week/', get_phase_workouts_by_week, name='workouts-by-week'),
    path('api/get-workout-log/<int:player_id>/<int:week>/<int:day>/', GetWorkoutLogView.as_view(), name='get-workout-log'),
    path('api/player-warmup/<int:player_id>/', PlayerWarmupView.as_view(), name='get-active-warmup'),
]