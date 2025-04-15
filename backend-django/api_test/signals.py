from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import PlayerArmCareRoutine, PlayerArmCareExercise, Player
from django.contrib.auth.models import User


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
        
@receiver(post_save, sender=User)
def create_or_update_player_for_user(sender, instance, created, **kwargs):
    if created:
        # Automatically create a Player instance for the new User
        Player.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )
    else:
        # Update the Player instance if the User is updated
        try:
            player = instance.player  # Assuming a OneToOne relationship
            player.first_name = instance.first_name
            player.last_name = instance.last_name
            player.email = instance.email
            player.save()
        except Player.DoesNotExist:
            # If the Player instance doesn't exist, create it
            Player.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email
            )        