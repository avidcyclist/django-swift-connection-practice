from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token



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
    ArmCareRoutineListView,
    ArmCareRoutineDetailView,
    PlayerArmCareRoutineListView,
    PlayerArmCareRoutineDetailView,
    ArmCareRoutineGroupedByDayView,
    PlayerArmCareRoutineGroupedByDayView,
    PasswordChangeView,
    CustomLoginView,
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
     # ArmCareRoutine URLs
    path("api/arm-care-routines/", ArmCareRoutineListView.as_view(), name="arm-care-routine-list"),
    path("api/arm-care-routines/<int:pk>/", ArmCareRoutineDetailView.as_view(), name="arm-care-routine-detail"),

    # PlayerArmCareRoutine URLs
    path("api/players/arm-care-routines/<int:player_id>/", PlayerArmCareRoutineListView.as_view(), name="player-arm-care-routine-list"),
    path("api/player-arm-care-routines/<int:pk>/", PlayerArmCareRoutineDetailView.as_view(), name="player-arm-care-routine-detail"),
    # New grouped-by-day views
    path("api/arm-care-routines/grouped-by-day/<int:routine_id>/", ArmCareRoutineGroupedByDayView.as_view(), name="arm-care-routine-grouped-by-day"),
    path("api/player-arm-care-routines/grouped-by-day/<int:routine_id>/", PlayerArmCareRoutineGroupedByDayView.as_view(), name="player-arm-care-routine-grouped-by-day"),
    #password views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/password-change/', PasswordChangeView.as_view(), name='password-change'),
    #login views
    path('api/login/', CustomLoginView.as_view(), name='api_login'),

]