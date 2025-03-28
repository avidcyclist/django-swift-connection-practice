from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Player, Workout, PlayerPhase, Phase, WorkoutLog
from .serializers import PlayerSerializer, WorkoutSerializer, PlayerPhaseSerializer, WorkoutLogSerializer

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
        player_phases = PlayerPhase.objects.filter(player__id=player_id)
        serializer = PlayerPhaseSerializer(player_phases, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def save_workout_log(request):
    print("Request data:", request.data)  # Debugging

    serializer = WorkoutLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Workout log saved successfully!"}, status=status.HTTP_201_CREATED)
    print("Validation errors:", serializer.errors)  # Debugging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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