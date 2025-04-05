from django.db import models
from django.contrib.auth.models import User  # Assuming Player is tied to the User model

# Create your models here.

class Workout(models.Model):
    exercise = models.CharField(max_length=100)
    youtube_link = models.URLField(blank=True, null=True)  # Optional field for YouTube link
    
    def __str__(self):
        return self.exercise
    
class Phase(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class PhaseWorkout(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="phase_workouts")  # Link to the phase
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Link to the workout
    reps = models.IntegerField()  # Reps for this workout in the phase
    sets = models.IntegerField()  # Sets for this workout in the phase
    week = models.IntegerField()  # Week of the phase (1, 2, 3, etc.)
    day = models.IntegerField()  # Day of the phase (1, 2, 3, etc.)
    order = models.IntegerField(default=1)  # Order of the workout in the day
    default_rpe = models.JSONField(default=list) 
    
    def __str__(self):
        return f"{self.phase.name} - {self.workout.exercise} ({self.sets} sets x {self.reps} reps)"
    
    
class Corrective(models.Model):
    name = models.CharField(max_length=100)  # Name of the corrective exercise
    sets = models.IntegerField(null=True, blank=True)  # Optional: Number of sets
    reps = models.IntegerField(null=True, blank=True)  # Optional: Number of reps
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return self.name
    
class ActiveWarmup(models.Model):
    name = models.CharField(max_length=100)  # Name of the active warmup exercise
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return self.name


class PowerCNSWarmup(models.Model):
    name = models.CharField(max_length=100)  # Name of the warmup (e.g., "Day 1 Power CNS Warmup")
    day = models.IntegerField()  # Day number (e.g., 1, 2, 3, 4)
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return f"{self.name} (Day {self.day})"


class PowerCNSExercise(models.Model):
    warmup = models.ForeignKey(PowerCNSWarmup, on_delete=models.CASCADE, related_name="exercises")  # Link to the warmup
    name = models.CharField(max_length=100)  # Name of the exercise
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return f"{self.name} ({self.warmup.name})"
    
    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.CharField(max_length=100)
    correctives = models.ManyToManyField(Corrective, blank=True, related_name="players")  # Many-to-Many relationship
    active_warmup = models.ManyToManyField(ActiveWarmup, blank=True, related_name="players")  # Many-to-Many relationship
    power_cns_warmups = models.ManyToManyField(PowerCNSWarmup, blank=True, related_name="players")  # Many-to-Many relationship


    def __str__(self):
        return self.name

class PlayerPhase(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  # Link to a player
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)    # Link to a phase
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.player.name} - {self.phase.name}"

    def save(self, *args, **kwargs):
        # Check if this is an update and the phase has changed
        if self.pk:  # If the instance already exists (not a new one)
            old_phase = PlayerPhase.objects.get(pk=self.pk).phase
            if old_phase != self.phase:  # If the phase has changed
                # Delete existing PlayerPhaseWorkout entries
                from .models import PlayerPhaseWorkout, PhaseWorkout  # Avoid circular imports
                PlayerPhaseWorkout.objects.filter(player_phase=self).delete()

                # Repopulate PlayerPhaseWorkout with defaults from the new phase
                phase_workouts = PhaseWorkout.objects.filter(phase=self.phase)
                for workout in phase_workouts:
                    PlayerPhaseWorkout.objects.create(
                        player_phase=self,
                        workout=workout.workout,
                        reps=workout.reps,
                        sets=workout.sets,
                        week=workout.week,
                        day=workout.day,
                        order=workout.order,
                        rpe=workout.default_rpe,
                        player_rpe=[None] * len(workout.default_rpe)  
                    )

        # Save the PlayerPhase instance
        super().save(*args, **kwargs)
    
class WorkoutLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)  # Link to the phase
    week = models.IntegerField()  # Week number within the phase
    day = models.IntegerField()   # Day number within the week
    exercises = models.JSONField()  # Store all exercises and their sets as a JSON object
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the log is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when the log is modified

    class Meta:
        unique_together = ('player', 'phase', 'week', 'day')  # Ensure no duplicate logs for the same week/day

    def __str__(self):
        return f"{self.player.user.username} - Phase: {self.phase.name}, Week: {self.week}, Day: {self.day}"
    
    
class PlayerPhaseWorkout(models.Model):
    player_phase = models.ForeignKey(
        PlayerPhase, 
        on_delete=models.CASCADE, 
        related_name="player_phase_workouts"
    )  # Link to the player's phase
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Link to the workout
    reps = models.IntegerField()  # Custom reps for this workout
    sets = models.IntegerField()  # Custom sets for this workout
    week = models.IntegerField()  # Week of the phase (1, 2, 3, etc.)hen
    day = models.IntegerField()  # Day of the phase (1, 2, 3, etc.)
    order = models.IntegerField(default=1)  # Order of the workout in the day
    rpe = models.JSONField(default=list)  # Custom RPE values
    player_rpe = models.JSONField(default=list, blank=True)  # Player-entered RPE values (mutable)

    def __str__(self):
        return f"{self.player_phase.player.name} - {self.workout.exercise} ({self.sets} sets x {self.reps} reps)"