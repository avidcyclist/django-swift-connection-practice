from rest_framework import serializers
from .models import Player, Workout

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'age', 'team']  # Include the fields you want in the API response

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['exercise', 'reps', 'sets']  # Include the fields you want in the API response