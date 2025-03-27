from rest_framework import serializers
from .models import Player, Workout, Phase, PlayerPhase, WorkoutLog, PhaseWorkout

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'age', 'team']  # Include the fields you want in the API response

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['exercise']  # Include the fields you want in the API response
   
        
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'player', 'workout', 'set_number', 'weight', 'rpe', 'date']
        
class PhaseWorkoutSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()  # Include workout details

    class Meta:
        model = PhaseWorkout
        fields = ['workout', 'reps', 'sets']
        
class PhaseSerializer(serializers.ModelSerializer):
    phase_workouts = PhaseWorkoutSerializer(many=True)  # Include workouts with reps and sets

    class Meta:
        model = Phase
        fields = ['name', 'phase_workouts']


class PlayerPhaseSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer()

    class Meta:
        model = PlayerPhase
        fields = ['player', 'phase', 'start_date', 'end_date']     