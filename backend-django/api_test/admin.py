from django.contrib import admin
from .models import Player, Workout, PlayerPhase, Phase, WorkoutLog, PhaseWorkout, Corrective, PlayerPhaseWorkout

admin.site.register(Player)

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    search_fields = ["exercise"]  # Allow searching by exercise name
admin.site.register(Phase)

admin.site.register(WorkoutLog)
admin.site.register(PhaseWorkout)
admin.site.register(Corrective)



# Inline admin for PlayerPhaseWorkout
class PlayerPhaseWorkoutInline(admin.TabularInline):
    model = PlayerPhaseWorkout
    extra = 0  # Do not show extra empty rows by default
    fields = ("workout", "week", "day", "order", "sets", "reps", "rpe")  # Fields to display
    can_delete = True  # Allow coaches to delete workouts

# Admin for PlayerPhase
@admin.register(PlayerPhase)
class PlayerPhaseAdmin(admin.ModelAdmin):
    list_display = ("player", "phase", "start_date", "end_date")  # Fields to display in the list view
    inlines = [PlayerPhaseWorkoutInline]  # Add the inline for PlayerPhaseWorkout

    # Override the change form to prepopulate PlayerPhaseWorkout if it doesn't exist
    def change_view(self, request, object_id, form_url="", extra_context=None):
        player_phase = self.get_object(request, object_id)

        # Check if PlayerPhaseWorkout entries already exist
        if not PlayerPhaseWorkout.objects.filter(player_phase=player_phase).exists():
            # Fetch workouts from the stock phase
            phase_workouts = PhaseWorkout.objects.filter(phase=player_phase.phase)
            for workout in phase_workouts:
                PlayerPhaseWorkout.objects.create(
                    player_phase=player_phase,
                    workout=workout.workout,
                    reps=workout.reps,
                    sets=workout.sets,
                    week=workout.week,
                    day=workout.day,
                    order=workout.order,
                    rpe=workout.default_rpe
                )

        return super().change_view(request, object_id, form_url, extra_context)