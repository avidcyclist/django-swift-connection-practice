from rest_framework import serializers
from .models import Player, Workout, Phase, PlayerPhase, WorkoutLog, PhaseWorkout, Corrective



class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'exercise']  # Include the fields you want in the API response
   
        
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'player', 'date', 'exercises']  # Replace individual fields with 'sets'
        
class PhaseWorkoutSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()  # Include workout details

    class Meta:
        model = PhaseWorkout
        fields = ['workout', 'reps', 'sets', 'week', 'day', 'order']  # Include reps, sets, day, and order
        
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
        
class CorrectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corrective
        fields = ['id', 'name', 'sets', 'reps', 'youtube_link']
                

class PlayerSerializer(serializers.ModelSerializer):
    correctives = CorrectiveSerializer(many=True)  # Include correctives in the player data

    class Meta:
        model = Player
        fields = ["id", "name", "age", "team", "correctives"]
        
class PhaseWorkoutsResponseSerializer(serializers.Serializer):
    phase_name = serializers.CharField()
    weeks = serializers.SerializerMethodField()

    def get_weeks(self, obj):
        weeks = {}
        for workout in obj['workouts']:
            week = workout.week
            day = workout.day
            if week not in weeks:
                weeks[week] = {"days": {}}
            if day not in weeks[week]["days"]:
                weeks[week]["days"][day] = []
            weeks[week]["days"][day].append(PhaseWorkoutSerializer(workout).data)
        return weeks