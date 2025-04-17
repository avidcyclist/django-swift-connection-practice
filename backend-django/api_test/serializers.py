from rest_framework import serializers
from django.contrib.auth.models import User

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
    ThrowingActiveWarmup,
    ArmCareRoutine,
    ArmCareExercise,
    PlayerArmCareRoutine,
    PlayerArmCareExercise,
    DailyIntake,
)

class ThrowingActiveWarmupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThrowingActiveWarmup
        fields = ['id', 'name', 'youtube_link', 'sets_reps']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'exercise', 'youtube_link']  # Include the fields you want in the API response
   
        
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'player', 'week', 'day', 'exercises', 'comments'] 
        
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
        fields = ["id", "first_name", "last_name", "age", "team"]  # Include active warmup and power CNS warmups
        
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
            "week_number",
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
            "week_number",
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
        
        
class ArmCareExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmCareExercise
        fields = ["id", "day", "focus", "exercise", "sets_reps", "youtube_link"]


class ArmCareRoutineSerializer(serializers.ModelSerializer):
    exercises = ArmCareExerciseSerializer(many=True, read_only=True)  # Include associated exercises

    class Meta:
        model = ArmCareRoutine
        fields = ["id", "name", "description", "exercises"]
        
class PlayerArmCareExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerArmCareExercise
        fields = ["id", "day", "focus", "exercise", "sets_reps", "youtube_link"]


class PlayerArmCareRoutineSerializer(serializers.ModelSerializer):
    exercises = PlayerArmCareExerciseSerializer(many=True, read_only=True)  # Include associated exercises
    player_name = serializers.CharField(source="player.__str__", read_only=True)  # Include player's name
    routine_name = serializers.CharField(source="routine.name", read_only=True)  # Include the name of the related ArmCareRoutine

    class Meta:
        model = PlayerArmCareRoutine
        fields = ["id", "player", "player_name", "routine_name", "description", "start_date", "end_date", "exercises"]
        
        
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
class CustomLoginSerializer(serializers.ModelSerializer):
    playerId = serializers.IntegerField(source='id', read_only=True)  # Assuming player_id is in a related profile model

    class Meta:
        model = User
        fields = ['playerId', 'first_name', 'last_name', 'email']
        
class DailyIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyIntake
        fields = [
            'id', 'player', 'date', 'arm_feel', 'body_feel', 'sleep_hours',
            'weight', 'met_calorie_macros', 'completed_day_plan', 'comments'
        ]
        read_only_fields = ['id', 'player']