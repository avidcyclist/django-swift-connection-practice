from django.contrib import admin
from .models import Player, Workout, PlayerPhase, Phase, WorkoutLog

admin.site.register(Player)
admin.site.register(Workout)
admin.site.register(Phase)
admin.site.register(PlayerPhase)
admin.site.register(WorkoutLog)