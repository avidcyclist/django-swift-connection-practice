from django.urls import path
from .views import PlayerInfoView, WorkoutView

urlpatterns = [
    path('api/player-info/', PlayerInfoView.as_view(), name='player-info'),
    path('api/player-workout/', WorkoutView.as_view(), name='player-workout'),
]