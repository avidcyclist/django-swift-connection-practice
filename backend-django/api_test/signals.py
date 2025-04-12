from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlayerArmCareRoutine, PlayerArmCareExercise

@receiver(post_save, sender=PlayerArmCareRoutine)
def copy_arm_care_exercises(sender, instance, created, **kwargs):
    if created:
        for exercise in instance.routine.exercises.all():
            PlayerArmCareExercise.objects.create(
                routine=instance,
                day=exercise.day,
                focus=exercise.focus,
                exercise=exercise.exercise,
                sets_reps=exercise.sets_reps,
                youtube_link=exercise.youtube_link,
            )