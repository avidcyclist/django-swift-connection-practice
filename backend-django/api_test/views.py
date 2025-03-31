from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Player, Workout, PlayerPhase, Phase, WorkoutLog, PhaseWorkout
from django.http import JsonResponse
from .serializers import PlayerSerializer, WorkoutSerializer, PlayerPhaseSerializer, WorkoutLogSerializer, CorrectiveSerializer

class PlayerInfoView(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

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
    date = request.data.get("date")

    if not player_id or not exercises or not date:
        return Response({"error": "Missing required fields (player, exercises, date)."}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the player exists
    player = get_object_or_404(Player, id=player_id)

    # Save the workout log
    workout_log = WorkoutLog.objects.create(player=player, date=date, exercises=exercises)
    return Response({"message": "Workout log saved successfully!"}, status=status.HTTP_201_CREATED)

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

    # Get the latest phase (or modify logic to select the desired phase)
    current_phase = player_phases.latest('start_date')

    # Group workouts by day and order them
    phase_workouts = PhaseWorkout.objects.filter(phase=current_phase.phase).order_by('day', 'order')
    grouped_workouts = {}
    for workout in phase_workouts:
        day = workout.day
        if day not in grouped_workouts:
            grouped_workouts[day] = []
        grouped_workouts[day].append({
            "exercise": workout.workout.exercise,
            "reps": workout.reps,
            "sets": workout.sets,
            "order": workout.order
        })

    # Convert defaultdict to a regular dict with integer keys
    response_data = {
        "phase_name": current_phase.phase.name,
        "workouts_by_day": {int(day): workouts for day, workouts in grouped_workouts.items()}
    }

    return JsonResponse(response_data)