
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404


from .models import (
    Player,
    Workout,
    PlayerPhase,
    WorkoutLog,
    PhaseWorkout,
    PlayerPhaseWorkout,
    PowerCNSWarmup,
    PlayerThrowingProgram,
    ThrowingProgram,
    Player,
    PlayerThrowingProgramDay,
    ThrowingRoutine,
    ArmCareRoutine,
    PlayerArmCareRoutine,
    PlayerArmCareExercise,
    DailyIntake,
)

from .serializers import (
    PlayerSerializer,
    WorkoutSerializer,
    WorkoutLogSerializer,
    CorrectiveSerializer,
    PlayerPhaseWorkoutSerializer,
    PhaseWorkoutSerializer,
    ActiveWarmupSerializer,
    ThrowingProgramSerializer,
    PlayerThrowingProgramSerializer,
    ThrowingRoutineSerializer,
    ThrowingActiveWarmupSerializer,
    PlayerThrowingProgramDaySerializer,
    ArmCareRoutineSerializer,
    PlayerArmCareRoutineSerializer,
    PlayerArmCareExerciseSerializer,
    ArmCareExerciseSerializer,
    PasswordChangeSerializer,
    CustomLoginSerializer,
    DailyIntakeSerializer,
)

class PlayerInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        try:
            player = request.user.player  # Get the Player instance associated with the authenticated user
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({"error": "Player not found for the authenticated user."}, status=404)

class WorkoutView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hello from the API Test App!"})

class PlayerPhaseView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def get(self, request):
        try:
            # Fetch all phases for the given player
            player = request.user.player  # Get the Player instance associated with the authenticated user
            player_phases = PlayerPhase.objects.filter(player=player)

            # Build the response data
            response_data = []
            for player_phase in player_phases:
                # Fetch workouts associated with the phase using PhaseWorkout
                phase_workouts = PhaseWorkout.objects.filter(phase=player_phase.phase)
                workouts_data = [
                    {
                        "exercise": phase_workout.workout.exercise,
                        "reps": phase_workout.reps,
                        "sets": phase_workout.sets,
                    }
                    for phase_workout in phase_workouts
                ]

                # Add phase and its workouts to the response
                response_data.append({
                    "phase_name": player_phase.phase.name,
                    "start_date": player_phase.start_date,
                    "end_date": player_phase.end_date,
                    "workouts": workouts_data,
                })
                

            return Response(response_data, status=status.HTTP_200_OK)
        except PlayerPhase.DoesNotExist:
            return Response({"error": "Player phases not found for the given player."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def save_workout_log(request):
    # Validate the incoming data
    data = request.data
    exercises = data.get("exercises")
    week = data.get("week")
    day = data.get("day")
    comments = data.get("comments", "")  # Get comments, default to an empty string if not provided

    if not exercises or not week or not day:
        return Response({"error": "Missing required fields (exercises, week, day)."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get the Player instance associated with the authenticated user
        player = request.user.player

        # Get the player's current phase
        player_phase = PlayerPhase.objects.filter(player=player).latest('start_date')

        # Check if a log already exists for this player, phase, week, and day
        workout_log, created = WorkoutLog.objects.update_or_create(
            player=player,
            phase=player_phase.phase,
            week=week,
            day=day,
            defaults={
                "exercises": exercises,
                "comments": comments,  # Add comments to the defaults
            }
        )

        # If the log already exists, update the comments and exercises
        if not created:
            workout_log.exercises = exercises
            workout_log.comments = comments
            workout_log.save()

        if created:
            return Response({"message": "Workout log created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Workout log updated successfully!"}, status=status.HTTP_200_OK)

    except PlayerPhase.DoesNotExist:
        return Response({"error": "No active phase found for the player."}, status=status.HTTP_404_NOT_FOUND)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_workout_logs(request):
    try:
        # Get the Player instance associated with the authenticated user
        player = request.user.player

        # Fetch workout logs for the player
        logs = WorkoutLog.objects.filter(player=player).order_by('-created_at')
        serializer = WorkoutLogSerializer(logs, many=True)
        return Response(serializer.data)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_players(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_player_correctives(request):
    try:
        player = request.user.player  # Get the authenticated user's player instance
        correctives = player.correctives.all()
        serializer = CorrectiveSerializer(correctives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_phase_workouts_by_day(request):
    try:
        player = request.user.player  # Get the authenticated user's player instance
        player_phases = PlayerPhase.objects.filter(player=player)
        if not player_phases.exists():
            return Response({"error": "No phases found for this player."}, status=status.HTTP_404_NOT_FOUND)

        current_phase = player_phases.latest('start_date')
        phase_workouts = PhaseWorkout.objects.filter(phase=current_phase.phase).order_by('day', 'order')
        grouped_workouts = {}
        for workout in phase_workouts:
            day = workout.day
            if day not in grouped_workouts:
                grouped_workouts[day] = []
            grouped_workouts[day].append(workout)

        response_data = {
            "phase_name": current_phase.phase.name,
            "workouts_by_day": {
                str(day): PhaseWorkoutSerializer(workouts, many=True).data
                for day, workouts in grouped_workouts.items()
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_phase_workouts_by_week(request):
    try:
        player = request.user.player  # Get the authenticated user's player instance
        player_phases = PlayerPhase.objects.filter(player=player)
        if not player_phases.exists():
            return Response({"error": "No phases found for this player."}, status=status.HTTP_404_NOT_FOUND)

        current_phase = player_phases.latest('start_date')
        player_phase_workouts = PlayerPhaseWorkout.objects.filter(player_phase=current_phase).order_by('week', 'day', 'order')
        grouped_workouts = {}
        for workout in player_phase_workouts:
            week = workout.week
            day = workout.day
            if week not in grouped_workouts:
                grouped_workouts[week] = {"days": {}}
            if day not in grouped_workouts[week]["days"]:
                grouped_workouts[week]["days"][day] = []
            grouped_workouts[week]["days"][day].append(workout)

        response_data = {
            "phase_name": current_phase.phase.name,
            "weeks": {
                str(week): {
                    "days": {
                        str(day): PlayerPhaseWorkoutSerializer(workouts, many=True).data
                        for day, workouts in week_data["days"].items()
                    }
                }
                for week, week_data in grouped_workouts.items()
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)


class GetWorkoutLogView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, week, day):
        try:
            player = request.user.player  # Get the authenticated user's player instance
            player_phase = PlayerPhase.objects.filter(player=player).latest('start_date')

            # Fetch the workout log for the player, phase, week, and day
            log = WorkoutLog.objects.filter(
                player=player,
                phase=player_phase.phase,
                week=week,
                day=day
            ).first()

            # Fetch the current workouts for the player's phase
            current_workouts = PlayerPhaseWorkout.objects.filter(
                player_phase=player_phase,
                week=week,
                day=day
            ).order_by('order')

            # If a log exists, adjust it to match the current workouts
            if log:
                log_data = WorkoutLogSerializer(log).data
                adjusted_exercises = []

                for workout in current_workouts:
                    exercise_log = next(
                        (e for e in log_data['exercises'] if e['exercise'] == workout.workout.exercise),
                        None
                    )

                    if exercise_log:
                        exercise_log['default_rpe'] = workout.rpe
                        exercise_log['player_rpe'] = workout.player_rpe
                        adjusted_exercises.append(exercise_log)
                    else:
                        adjusted_exercises.append({
                            "exercise": workout.workout.exercise,
                            "default_rpe": workout.rpe,
                            "player_rpe": [None] * len(workout.rpe),
                            "sets": [
                                {"weight": 0.0, "set_number": i + 1, "rpe": 0.0}
                                for i in range(workout.sets)
                            ]
                        })

                log_data['exercises'] = adjusted_exercises
                return Response(log_data, status=status.HTTP_200_OK)

            # If no log exists, return a default response with the current workouts
            default_exercises = [
                {
                    "exercise": workout.workout.exercise,
                    "default_rpe": workout.rpe,
                    "player_rpe": [None] * len(workout.rpe),
                    "sets": [
                        {"weight": None, "set_number": i + 1, "rpe": None}
                        for i in range(workout.sets)
                    ]
                }
                for workout in current_workouts
            ]

            return Response({
                "id": None,
                "player": player.id,
                "week": week,
                "day": day,
                "exercises": default_exercises
            }, status=status.HTTP_200_OK)

        except PlayerPhase.DoesNotExist:
            return Response({"error": "No active phase found for the player."}, status=status.HTTP_404_NOT_FOUND)
        
class PlayerWarmupView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        try:
            player = request.user.player  # Get the authenticated user's player instance

            # Fetch active warmups
            active_warmups = ActiveWarmupSerializer(player.active_warmup.all(), many=True).data

            # Fetch power CNS warmups
            power_cns_warmups = PowerCNSWarmup.objects.all().order_by("day")
            power_cns_warmups_data = [
                {
                    "id": warmup.id,
                    "name": warmup.name,
                    "day": warmup.day,
                    "youtube_link": warmup.youtube_link
                }
                for warmup in power_cns_warmups
            ]

            return Response({
                "active_warmups": active_warmups,
                "power_cns_warmups": power_cns_warmups_data
            }, status=status.HTTP_200_OK)

        except Player.DoesNotExist:
            return Response({"error": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
        
# List all throwing programs
class ThrowingProgramListView(generics.ListAPIView):
    queryset = ThrowingProgram.objects.all()
    serializer_class = ThrowingProgramSerializer


# Retrieve a specific throwing program
class ThrowingProgramDetailView(generics.RetrieveAPIView):
    queryset = ThrowingProgram.objects.all()
    serializer_class = ThrowingProgramSerializer
    
# Retrieve a specific player-specific program
class PlayerThrowingProgramListView(generics.ListAPIView):
    serializer_class = PlayerThrowingProgramSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        player = self.request.user.player  # Get the authenticated user's player instance
        return PlayerThrowingProgram.objects.filter(player=player)


# Assign a base program to a player
class AssignThrowingProgramView(generics.CreateAPIView):
    serializer_class = PlayerThrowingProgramSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def create(self, request, *args, **kwargs):
        program_id = request.data.get("program_id")

        try:
            player = request.user.player  # Get the authenticated user's player instance
            base_program = ThrowingProgram.objects.get(id=program_id)

            # Create a new player-specific program
            player_program = PlayerThrowingProgram.objects.create(
                player=player,
                program=base_program,
                start_date=base_program.start_date,
                end_date=base_program.end_date,
            )

            # Copy the days from the base program
            base_days = base_program.days.all()
            for base_day in base_days:
                player_day = PlayerThrowingProgramDay.objects.create(
                    player_program=player_program,
                    day_number=base_day.day_number,
                    name=base_day.name,
                    warmup=base_day.warmup,
                    throwing=base_day.throwing,
                    velo_command=base_day.velo_command,
                    arm_care=base_day.arm_care,
                    lifting=base_day.lifting,
                    conditioning=base_day.conditioning,
                )
                player_day.plyos.set(base_day.plyos.all())

            serializer = self.get_serializer(player_program)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ThrowingProgram.DoesNotExist:
            return Response({"error": "Base program not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
# List all throwing routines
class ThrowingRoutineListView(generics.ListAPIView):
    queryset = ThrowingRoutine.objects.all()
    serializer_class = ThrowingRoutineSerializer


# Retrieve a specific throwing routine
class ThrowingRoutineDetailView(generics.RetrieveAPIView):
    queryset = ThrowingRoutine.objects.all()
    serializer_class = ThrowingRoutineSerializer
    
# Retrieve a specific player-specific program
class PlayerThrowingProgramDetailView(generics.RetrieveAPIView):
    queryset = PlayerThrowingProgram.objects.all()
    serializer_class = PlayerThrowingProgramSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_player_throwing_active_warmups(request):
    try:
        player = request.user.player  # Get the authenticated user's player instance
        warmups = player.throwing_active_warmups.all()
        serializer = ThrowingActiveWarmupSerializer(warmups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({"error": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_player_throwing_program_weeks(request, program_id):
    try:
        player = request.user.player  # Get the authenticated user's player instance
        days = PlayerThrowingProgramDay.objects.filter(player_program__player=player, player_program_id=program_id).order_by('week_number', 'day_number')
        weeks = {}
        for day in days:
            week = day.week_number
            if week not in weeks:
                weeks[week] = []
            weeks[week].append(PlayerThrowingProgramDaySerializer(day).data)
        return Response(weeks, status=status.HTTP_200_OK)
    except PlayerThrowingProgramDay.DoesNotExist:
        return Response({"error": "Program not found."}, status=status.HTTP_404_NOT_FOUND)
    
# List all ArmCareRoutines
class ArmCareRoutineListView(generics.ListAPIView):
    queryset = ArmCareRoutine.objects.all()
    serializer_class = ArmCareRoutineSerializer


# Retrieve a specific ArmCareRoutine
class ArmCareRoutineDetailView(generics.RetrieveAPIView):
    queryset = ArmCareRoutine.objects.all()
    serializer_class = ArmCareRoutineSerializer
    
class PlayerArmCareRoutineListView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        try:
            player = request.user.player  # Get the authenticated user's player instance
            player_routines = PlayerArmCareRoutine.objects.filter(player=player)
            if player_routines.exists():
                serializer = PlayerArmCareRoutineSerializer(player_routines, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                default_routines = ArmCareRoutine.objects.all()
                serializer = ArmCareRoutineSerializer(default_routines, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response({"error": "Player not found."}, status=status.HTTP_404_NOT_FOUND)

# Retrieve a specific PlayerArmCareRoutine
class PlayerArmCareRoutineDetailView(generics.RetrieveAPIView):
    queryset = PlayerArmCareRoutine.objects.all()
    serializer_class = PlayerArmCareRoutineSerializer

class ArmCareRoutineGroupedByDayView(APIView):
    def get(self, request, routine_id):
        try:
            routine = ArmCareRoutine.objects.get(id=routine_id)
            exercises = routine.exercises.all().order_by("day")
            grouped_exercises = {}
            for exercise in exercises:
                day = exercise.day
                if day not in grouped_exercises:
                    grouped_exercises[day] = []
                grouped_exercises[day].append(ArmCareExerciseSerializer(exercise).data)

            response_data = {
                "id": routine.id,
                "name": routine.name,
                "description": routine.description,
                "days": grouped_exercises,
            }
            return Response(response_data, status=200)
        except ArmCareRoutine.DoesNotExist:
            return Response({"error": "Routine not found."}, status=404)


class PlayerArmCareRoutineGroupedByDayView(APIView):
    def get(self, request, routine_id):
        try:
            # Fetch the PlayerArmCareRoutine
            routine = PlayerArmCareRoutine.objects.get(id=routine_id)

            # Fetch and group exercises by day
            exercises = routine.exercises.all().order_by("day")
            grouped_exercises = {}
            for exercise in exercises:
                day = exercise.day
                if day not in grouped_exercises:
                    grouped_exercises[day] = []
                grouped_exercises[day].append(PlayerArmCareExerciseSerializer(exercise).data)

            # Prepare the response
            response_data = {
                "id": routine.id,
                "player": routine.player.id,
                "player_name": f"{routine.player.first_name} {routine.player.last_name}",
                "routine_name": routine.routine.name,  # Fetch the name from the related ArmCareRoutine
                "description": routine.description,
                "start_date": routine.start_date,
                "end_date": routine.end_date,
                "days": grouped_exercises,
            }
            return Response(response_data, status=200)

        except PlayerArmCareRoutine.DoesNotExist:
            return Response({"error": "Routine not found."}, status=404)
        
class EditPlayerArmCareRoutineView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        routine_id = request.data.get("routine_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        exercises = request.data.get("exercises")

        try:
            player = request.user.player  # Get the authenticated user's player instance
            routine = ArmCareRoutine.objects.get(id=routine_id)

            # Check if a PlayerArmCareRoutine already exists
            player_routine, created = PlayerArmCareRoutine.objects.get_or_create(
                player=player,
                routine=routine,
                defaults={"start_date": start_date, "end_date": end_date},
            )

            if not created:
                # Update the start and end dates if the routine already exists
                player_routine.start_date = start_date
                player_routine.end_date = end_date
                player_routine.save()

            # Clear existing exercises and add the edited ones
            PlayerArmCareExercise.objects.filter(routine=player_routine).delete()
            for exercise in exercises:
                PlayerArmCareExercise.objects.create(
                    routine=player_routine,
                    day=exercise["day"],
                    focus=exercise["focus"],
                    exercise=exercise["exercise"],
                    sets_reps=exercise["sets_reps"],
                    youtube_link=exercise["youtube_link"],
                )

            return Response({"message": "Routine updated successfully!"}, status=status.HTTP_200_OK)

        except Player.DoesNotExist:
            return Response({"error": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
        except ArmCareRoutine.DoesNotExist:
            return Response({"error": "Arm care routine not found."}, status=status.HTTP_404_NOT_FOUND)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."})
        return Response(serializer.errors, status=400)
    

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        player = Player.objects.get(user=user)  # Fetch the Player instance
        serializer = CustomLoginSerializer(player)
        return Response({
            'token': token.key,
            'user': serializer.data
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_daily_intakes(request):
    try:
        player = request.user.player  # Get the Player instance associated with the authenticated user
        logs = DailyIntake.objects.filter(player=player).order_by('-date')
        serializer = DailyIntakeSerializer(logs, many=True)
        return Response(serializer.data)
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def save_daily_intake(request):
    data = request.data

    try:
        # Get the Player instance associated with the authenticated user
        player = request.user.player
    except Player.DoesNotExist:
        return Response({"error": "Player not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

    date = data.get('date', None)
    if not date:
        return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Round sleep_hours and weight to 2 decimal places before saving
    sleep_hours = round(float(data.get('sleep_hours', 0)), 2) if data.get('sleep_hours') else None
    weight = round(float(data.get('weight', 0)), 2) if data.get('weight') else None

    # Use update_or_create to handle both create and update
    daily_intake, created = DailyIntake.objects.update_or_create(
        player=player,
        date=date,
        defaults={
            'arm_feel': data.get('arm_feel'),
            'body_feel': data.get('body_feel'),
            'sleep_hours': sleep_hours,
            'weight': weight,
            'met_calorie_macros': data.get('met_calorie_macros'),
            'completed_day_plan': data.get('completed_day_plan'),
            'comments': data.get('comments'),
        }
    )

    serializer = DailyIntakeSerializer(daily_intake)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
