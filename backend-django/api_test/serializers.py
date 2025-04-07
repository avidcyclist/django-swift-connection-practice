from rest_framework import serializers
from .models import (
    Player,
    Workout,
    ActiveWarmup,
    PowerCNSWarmup,
    PowerCNSExercise,
    Phase,
    PlayerPhase,
    WorkoutLog,
    PhaseWorkout,
    Corrective,
    PlayerPhaseWorkout,
    ThrowingRoutine,
    ThrowingProgram,
    ThrowingProgramDay,
    PlayerThrowingProgram,
    PlayerThrowingProgramDay,
    Drill,
)



class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'exercise', 'youtube_link']  # Include the fields you want in the API response
   
        
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'player', 'week', 'day', 'exercises'] 
        
class PhaseWorkoutSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()  # Include workout details
    default_rpe = serializers.JSONField()  # Include default_rpe field
    
    class Meta:
        model = PhaseWorkout
        fields = ['workout', 'reps', 'sets', 'week', 'day', 'order', 'default_rpe']  # Include reps, sets, day, and order
        
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

    class Meta:
        model = Player
        fields = ["id", "name", "age", "team"]  # Include active warmup and power CNS warmups
        
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
    
    
class PlayerPhaseWorkoutSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()  # Include workout details (e.g., exercise name, YouTube link)

    class Meta:
        model = PlayerPhaseWorkout
        fields = ['workout', 'sets', 'reps', 'rpe', 'week', 'day', 'order']
        
        
class ActiveWarmupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveWarmup
        fields = ["id", "name", "youtube_link"]
        
class PowerCNSExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerCNSExercise
        fields = ["id", "name", "youtube_link"]
        
        
class PowerCNSWarmupSerializer(serializers.ModelSerializer):
    exercises = PowerCNSExerciseSerializer(many=True)  # Include exercises in the warmup

    class Meta:
        model = PowerCNSWarmup
        fields = ["id", "name", "day", "exercises"]
        
class DrillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drill
        fields = ["id", "name", "sets_reps", "weight", "distance", "throws", "rpe", "video_link"]


class ThrowingRoutineSerializer(serializers.ModelSerializer):
    drills = DrillSerializer(many=True, read_only=True)  # Include associated drills

    class Meta:
        model = ThrowingRoutine
        fields = ["id", "name", "description", "drills"]
        
class ThrowingProgramDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = ThrowingProgramDay
        fields = [
            "id",
            "day_number",
            "name",
            "warmup",
            "plyos",
            "throwing",
            "velo_command",
            "arm_care",
            "lifting",
            "conditioning",
        ]
        
class ThrowingProgramSerializer(serializers.ModelSerializer):
    days = ThrowingProgramDaySerializer(many=True, read_only=True)  # Include program days

    class Meta:
        model = ThrowingProgram
        fields = ["id", "name", "days"]
        
class PlayerThrowingProgramDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerThrowingProgramDay
        fields = [
            "id",
            "day_number",
            "name",
            "warmup",
            "plyos",
            "throwing",
            "velo_command",
            "arm_care",
            "lifting",
            "conditioning",
        ]
        
class PlayerThrowingProgramSerializer(serializers.ModelSerializer):
    days = PlayerThrowingProgramDaySerializer(many=True, read_only=True)  # Include player program days

    class Meta:
        model = PlayerThrowingProgram
        fields = ["id", "player", "program", "start_date", "end_date", "days"]