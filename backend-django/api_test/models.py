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
    
    
    