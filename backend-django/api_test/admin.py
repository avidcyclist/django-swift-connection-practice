from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .utils import clone_arm_care_routine_for_player
from django.shortcuts import get_object_or_404

from .models import (
    Player,
    ActiveWarmup,
    PowerCNSExercise,
    PowerCNSWarmup,
    Workout,
    PlayerPhase,
    Phase,
    WorkoutLog,
    PhaseWorkout,
    Corrective,
    PlayerPhaseWorkout,
    ThrowingRoutine,
    Drill,
    ThrowingProgram,
    ThrowingProgramDay,
    PlayerThrowingProgram,
    PlayerThrowingProgramDay,
    ThrowingActiveWarmup,
    ArmCareRoutine,
    PlayerArmCareExercise,
    PlayerArmCareRoutine,
    ArmCareExercise,
)

@admin.register(ActiveWarmup)
class ActiveWarmupAdmin(admin.ModelAdmin):
    list_display = ("name", "youtube_link")
    search_fields = ("name",)


class PowerCNSExerciseInline(admin.TabularInline):
    model = PowerCNSExercise
    extra = 0


@admin.register(PowerCNSWarmup)
class PowerCNSWarmupAdmin(admin.ModelAdmin):
    list_display = ("name", "day", "youtube_link")
    inlines = [PowerCNSExerciseInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "age", "team")  # Updated fields
    filter_horizontal = ("correctives", "active_warmup", "power_cns_warmups", "throwing_active_warmups", "arm_care_routines")  # Include throwing_active_warmups
    search_fields = ("first_name", "last_name", "email", "team")  # Add search functionality

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    search_fields = ["exercise"]  # Allow searching by exercise name
admin.site.register(Phase)

admin.site.register(WorkoutLog)
admin.site.register(PhaseWorkout)
admin.site.register(Corrective)




# Inline admin for Drill (to manage drills within a routine)
class DrillInline(admin.TabularInline):
    model = Drill
    extra = 0  # Do not show extra empty rows by default
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["name"].required = False  # Make 'name' optional
        formset.form.base_fields["sets_reps"].required = False  # Make 'sets_reps' optional
        return formset

# Admin for ThrowingRoutine with inline drills
@admin.register(ThrowingRoutine)
class ThrowingRoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [DrillInline]


# Inline admin for ThrowingProgramDay (to manage days within a program)
class ThrowingProgramDayInline(admin.TabularInline):
    model = ThrowingProgramDay
    extra = 0  # Do not show extra empty rows by default
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},  # Compact text fields
    }    

# Admin for ThrowingProgram with inline days
@admin.register(ThrowingProgram)
class ThrowingProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [ThrowingProgramDayInline]


# Admin for PlayerThrowingProgramDay
@admin.register(PlayerThrowingProgramDay)
class PlayerThrowingProgramDayAdmin(admin.ModelAdmin):
    list_display = ("player_program", "day_number", "name")
    search_fields = ("player_program__player__name", "name")



# Inline admin for PlayerPhaseWorkout
class PlayerPhaseWorkoutInline(admin.TabularInline):
    model = PlayerPhaseWorkout
    extra = 0  # Do not show extra empty rows by default
    fields = ("workout", "week", "day", "order", "sets", "reps", "rpe")  # Fields to display
    can_delete = True  # Allow coaches to delete workouts
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "workout":
            # Order workouts alphabetically by exercise name
            kwargs["queryset"] = Workout.objects.order_by("exercise")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    
    
        
class PlayerThrowingProgramDayInline(admin.TabularInline):
    model = PlayerThrowingProgramDay
    extra = 0  # Do not show extra empty rows by default
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},  # Compact text fields
    }
    
    
@admin.register(PlayerThrowingProgram)
class PlayerThrowingProgramAdmin(admin.ModelAdmin):
    list_display = ("player", "program", "start_date", "end_date")
    inlines = [PlayerThrowingProgramDayInline]

    def save_model(self, request, obj, form, change):
        # Check if the program has changed
        if change:
            # Get the original program before the change
            original_program = PlayerThrowingProgram.objects.get(pk=obj.pk).program

            # If the program has changed, update the associated days
            if obj.program != original_program:
                # Delete existing PlayerThrowingProgramDay entries
                PlayerThrowingProgramDay.objects.filter(player_program=obj).delete()

                # Populate new days from the new program
                base_program = obj.program
                base_days = base_program.days.all()
                for base_day in base_days:
                    PlayerThrowingProgramDay.objects.create(
                        player_program=obj,
                        week_number=base_day.week_number,
                        day_number=base_day.day_number,
                        name=base_day.name,
                        warmup=base_day.warmup,
                        plyos=base_day.plyos,  # Directly copy the string value
                        throwing=base_day.throwing,
                        velo_command=base_day.velo_command,
                        arm_care=base_day.arm_care,
                        lifting=base_day.lifting,
                        conditioning=base_day.conditioning,
                    )

        # Save the PlayerThrowingProgram object
        super().save_model(request, obj, form, change)

        # If this is a new program, populate it with data from the base program
        if not change:  # Only for new objects
            base_program = obj.program
            base_days = base_program.days.all()
            for base_day in base_days:
                PlayerThrowingProgramDay.objects.create(
                    player_program=obj,
                    week_number=base_day.week_number,
                    day_number=base_day.day_number,
                    name=base_day.name,
                    warmup=base_day.warmup,
                    plyos=base_day.plyos,  # Directly copy the string value
                    throwing=base_day.throwing,
                    velo_command=base_day.velo_command,
                    arm_care=base_day.arm_care,
                    lifting=base_day.lifting,
                    conditioning=base_day.conditioning,
                )

admin.site.unregister(PlayerThrowingProgramDay)

@admin.register(ThrowingActiveWarmup)
class ThrowingActiveWarmupAdmin(admin.ModelAdmin):
    list_display = ("name", "youtube_link", "sets_reps")  # Include sets_reps in the list view
    search_fields = ("name", "sets_reps")  # Allow searching by name and sets_reps
    
    
class ArmCareExerciseInline(admin.TabularInline):
    model = ArmCareExercise
    extra = 1


class PlayerArmCareExerciseInline(admin.TabularInline):
    model = PlayerArmCareExercise
    extra = 1

@admin.register(PlayerArmCareRoutine)
class PlayerArmCareRoutineAdmin(admin.ModelAdmin):
    list_display = ("player", "name", "description")
    inlines = [PlayerArmCareExerciseInline]
    

from django import forms
from .models import Player

class CustomizeForPlayerForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Player.objects.all(), label="Select Player")
    
@admin.action(description="Customize for Player")
def customize_for_player(modeladmin, request, queryset):
    """
    Admin action to clone an ArmCareRoutine for a specific player.
    """
    if "apply" in request.POST:
        # Handle form submission
        form = CustomizeForPlayerForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data["player"]
            for routine in queryset:
                clone_arm_care_routine_for_player(player, routine)
            modeladmin.message_user(request, "Selected routines have been customized for the player.")
            return

    else:
        # Display the form
        form = CustomizeForPlayerForm()

    # Render the form in the admin panel
    return admin.helpers.ActionFormResponse(
        request,
        form=form,
        title="Customize Arm Care Routine for Player",
        action="customize_for_player",
        queryset=queryset,
    )

@admin.register(ArmCareRoutine)
class ArmCareRoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [ArmCareExerciseInline]
    actions = [customize_for_player]
    
