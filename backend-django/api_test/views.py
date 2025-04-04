from django.shortcuts import render
import json
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Player, Workout, PlayerPhase, Phase, WorkoutLog, PhaseWorkout, PlayerPhaseWorkout
from django.http import JsonResponse
from .serializers import PlayerSerializer, WorkoutSerializer, PlayerPhaseSerializer, WorkoutLogSerializer, CorrectiveSerializer, PlayerPhaseWorkoutSerializer, PhaseWorkoutSerializer, PhaseWorkoutsResponseSerializer, ActiveWarmupSerializer, PowerCNSWarmupSerializer

class PlayerInfoView(APIView):
    def get(self, request, player_id):
        try:
            # Get the player by ID
            player = Player.objects.get(id=player_id)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({"error": "Player not found."}, status=404)

class WorkoutView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hello from the API Test App!"})

class PlayerPhaseView(APIView):
    def get(self, request, player_id):
        try:
            # Fetch all phases for the given player
            player_phases = PlayerPhase.objects.filter(player__id=player_id)

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
def save_workout_log(request):
    print("Request data:", request.data)  # Debugging

    # Validate the incoming data
    player_id = request.data.get("player")
    exercises = request.data.get("exercises")
    week = request.data.get("week")
    day = request.data.get("day")

    if not player_id or not exercises or not week or not day:
        return Response({"error": "Missing required fields (player, exercises, week, day)."}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the player exists
    player = get_object_or_404(Player, id=player_id)

    # Get the player's current phase
    player_phase = PlayerPhase.objects.filter(player=player).latest('start_date')

    # Check if a log already exists for this player, phase, week, and day
    workout_log, created = WorkoutLog.objects.update_or_create(
        player=player,
        phase=player_phase.phase,
        week=week,
        day=day,
        defaults={"exercises": exercises}
    )

    if created:
        return Response({"message": "Workout log created successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Workout log updated successfully!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_workout_logs(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    logs = WorkoutLog.objects.filter(player_id=player_id).order_by('-date')
    serializer = WorkoutLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_players(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_player_id(request):
    # Temporarily return a hard-coded playerId for testing
    return Response({"playerId": 1}, status=200)


@api_view(['GET'])
def get_player_correctives(request, player_id):
    # Fetch the player or return a 404 if not found
    player = get_object_or_404(Player, id=player_id)

    # Get the correctives assigned to the player
    correctives = player.correctives.all()

    serializer = CorrectiveSerializer(correctives, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_phase_workouts_by_day(request, player_id):
    # Get the player's current phase
    player_phases = PlayerPhase.objects.filter(player__id=player_id)
    if not player_phases.exists():
        return Response({"error": "No phases found for this player."}, status=status.HTTP_404_NOT_FOUND)

    # Get the latest phase
    current_phase = player_phases.latest('start_date')

    # Group workouts by day
    phase_workouts = PhaseWorkout.objects.filter(phase=current_phase.phase).order_by('day', 'order')
    grouped_workouts = {}
    for workout in phase_workouts:
        day = workout.day
        if day not in grouped_workouts:
            grouped_workouts[day] = []
        grouped_workouts[day].append(workout)

    # Serialize the response
    response_data = {
        "phase_name": current_phase.phase.name,
        "workouts_by_day": {
            str(day): PhaseWorkoutSerializer(workouts, many=True).data
            for day, workouts in grouped_workouts.items()
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_phase_workouts_by_week(request, player_id):
    # Get the player's current phase
    player_phases = PlayerPhase.objects.filter(player__id=player_id)
    if not player_phases.exists():
        return Response({"error": "No phases found for this player."}, status=status.HTTP_404_NOT_FOUND)

    # Get the latest phase
    current_phase = player_phases.latest('start_date')

    # Group workouts by week and day
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

    # Serialize the response
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


class GetWorkoutLogView(APIView):
    def get(self, request, player_id, week, day):
        # Get the player's current phase
        player_phase = PlayerPhase.objects.filter(player__id=player_id).latest('start_date')

        # Fetch the workout log for the player, phase, week, and day
        log = WorkoutLog.objects.filter(
            player_id=player_id,
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
                # Find the matching exercise in the log
                exercise_log = next(
                    (e for e in log_data['exercises'] if e['exercise'] == workout.workout.exercise),
                    None
                )

                if exercise_log:
                    # Adjust the sets if they don't match
                    while len(exercise_log['sets']) < workout.sets:
                        exercise_log['sets'].append({
                            "weight": 0.0,
                            "set_number": len(exercise_log['sets']) + 1,
                            "rpe": 0.0
                        })
                    while len(exercise_log['sets']) > workout.sets:
                        exercise_log['sets'].pop()

                    # Add default RPE to the exercise log
                    exercise_log['default_rpe'] = workout.rpe  # Add default RPE from PlayerPhaseWorkout
                    adjusted_exercises.append(exercise_log)
                else:
                    # Add a new exercise if it wasn't in the log
                    adjusted_exercises.append({
                        "exercise": workout.workout.exercise,
                        "default_rpe": workout.rpe,  # Add default RPE from PlayerPhaseWorkout
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
                "default_rpe": workout.rpe,  # Add default RPE from PlayerPhaseWorkout
                "sets": [
                    {"weight": None, "set_number": i + 1, "rpe": None}
                    for i in range(workout.sets)
                ]
            }
            for workout in current_workouts
        ]

        return Response({
            "id": None,
            "player": player_id,
            "week": week,
            "day": day,
            "exercises": default_exercises
        }, status=status.HTTP_200_OK)
        
        
class PlayerWarmupView(APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(id=player_id)
            active_warmups = ActiveWarmupSerializer(player.active_warmup.all(), many=True).data
            power_cns_warmups = PowerCNSWarmupSerializer(player.power_cns_warmups.all(), many=True).data
            return Response({
                "active_warmups": active_warmups,
                "power_cns_warmups": power_cns_warmups
            }, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response({"error": "Player not found."}, status=status.HTTP_404_NOT_FOUND)