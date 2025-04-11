from django.urls import path
from .views import (
    PlayerInfoView,
    WorkoutView,
    PlayerPhaseView,
    PlayerWarmupView,
    GetWorkoutLogView,
    save_workout_log,
    get_workout_logs,
    get_phase_workouts_by_week,
    get_players,
    get_player_correctives,
    get_phase_workouts_by_day,
    ThrowingProgramListView,
    ThrowingProgramDetailView,
    PlayerThrowingProgramListView,
    PlayerThrowingProgramDetailView,
    AssignThrowingProgramView,
    ThrowingRoutineListView,
    ThrowingRoutineDetailView,
    get_player_throwing_active_warmups,
    get_player_throwing_program_weeks,
)

urlpatterns = [
    path('api/player-info/<int:player_id>/', PlayerInfoView.as_view(), name='player-info'),
    path('api/player-workout/', WorkoutView.as_view(), name='player-workout'),
    path('api/player-phases/<int:player_id>/', PlayerPhaseView.as_view(), name='player-phases'),
    path('api/save-workout-log/', save_workout_log, name='save-workout-log'),
    path('api/get-workout-logs/<int:player_id>/', get_workout_logs, name='get-workout-logs'),
    path('api/players/', get_players, name='get_players'),
    path('api/player/<int:player_id>/correctives/', get_player_correctives, name='get-player-correctives'),
    path('api/player-phases/<int:player_id>/workouts-by-day/', get_phase_workouts_by_day, name='workouts-by-day'),
    path('api/player-phases/<int:player_id>/workouts-by-week/', get_phase_workouts_by_week, name='workouts-by-week'),
    path('api/get-workout-log/<int:player_id>/<int:week>/<int:day>/', GetWorkoutLogView.as_view(), name='get-workout-log'),
    path('api/player-warmup/<int:player_id>/', PlayerWarmupView.as_view(), name='get-active-warmup'),
    #throwing views
    path("api/throwing-programs/", ThrowingProgramListView.as_view(), name="throwing-program-list"),
    path("api/throwing-programs/<int:pk>/", ThrowingProgramDetailView.as_view(), name="throwing-program-detail"),
    path("api/player-throwing-programs/", PlayerThrowingProgramListView.as_view(), name="player-throwing-program-list"),
    path("api/player-throwing-programs/<int:pk>/", PlayerThrowingProgramDetailView.as_view(), name="player-throwing-program-detail"),
    path("api/assign-throwing-program/", AssignThrowingProgramView.as_view(), name="assign-throwing-program"),
    # Throwing routines
    path("api/throwing-routines/", ThrowingRoutineListView.as_view(), name="throwing-routine-list"),
    path("api/throwing-routines/<int:pk>/", ThrowingRoutineDetailView.as_view(), name="throwing-routine-detail"),
    path('api/player/throwing-active-warmups/<int:player_id>/', get_player_throwing_active_warmups, name='get-player-throwing-active-warmups'),
    path('api/player-throwing-programs/weeks/<int:program_id>/', get_player_throwing_program_weeks, name='get-player-throwing-program-weeks'),

]