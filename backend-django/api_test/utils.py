from .models import PlayerArmCareRoutine, PlayerArmCareExercise

def clone_arm_care_routine_for_player(player, routine):
    """
    Clone an ArmCareRoutine into a PlayerArmCareRoutine for a specific player.
    """
    # Create a customized routine for the player
    custom_routine = PlayerArmCareRoutine.objects.create(
        player=player,
        name=f"{routine.name} (Customized)",
        description=routine.description,
    )

    # Copy all exercises from the standard routine to the customized routine
    for exercise in routine.exercises.all():
        PlayerArmCareExercise.objects.create(
            routine=custom_routine,
            focus=exercise.focus,
            exercise=exercise.exercise,
            sets_reps=exercise.sets_reps,
            youtube_link=exercise.youtube_link,
        )

    return custom_routine