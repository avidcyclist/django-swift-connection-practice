from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Workout(models.Model):
    exercise = models.CharField(max_length=100)
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return self.exercise
    
class Phase(models.Model):
    name = models.CharField(max_length=100)
    workouts = models.ManyToManyField(Workout)  # A phase can have multiple workouts

    def __str__(self):
        return self.name

class PlayerPhase(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  # Link to a player
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)    # Link to a phase
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.player.name} - {self.phase.name}" 