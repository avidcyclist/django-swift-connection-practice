from rest_framework import serializers
from .models import Player, Workout, Phase, PlayerPhase, WorkoutLog

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'age', 'team']  # Include the fields you want in the API response

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['exercise', 'reps', 'sets']  # Include the fields you want in the API response
        
class PhaseSerializer(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True)

    class Meta:
        model = Phase
        fields = ['name', 'workouts']

class PlayerPhaseSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer()

    class Meta:
        model = PlayerPhase
        fields = ['player', 'phase', 'start_date', 'end_date']        
        
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'player', 'workout', 'set_number', 'weight', 'rpe', 'date']