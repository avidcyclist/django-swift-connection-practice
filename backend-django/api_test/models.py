from django.db import models
from django.contrib.auth.models import User  # Assuming Player is tied to the User model

# Create your models here.

class Workout(models.Model):
    exercise = models.CharField(max_length=100)

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
    
    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.CharField(max_length=100)
    correctives = models.ManyToManyField(Corrective, blank=True, related_name="players")  # Many-to-Many relationship

    def __str__(self):
        return self.name

class PlayerPhase(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  # Link to a player
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)    # Link to a phase
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.player.name} - {self.phase.name}" 
    
class WorkoutLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    exercises = models.JSONField()  # Store all exercises and their sets as a JSON object

    def __str__(self):
        return f"{self.player.user.username} - {self.date} - {len(self.exercises)} exercises"