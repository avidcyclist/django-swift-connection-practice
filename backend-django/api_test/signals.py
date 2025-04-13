from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
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
            
@receiver(user_logged_in)
def update_password_changed_flag(sender, request, user, **kwargs):
    if hasattr(user, 'profile') and not user.profile.password_changed:
        user.profile.password_changed = True
        user.profile.save()