from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player, Workout, PlayerPhase, Phase
from .serializers import PlayerSerializer, WorkoutSerializer, PlayerPhaseSerializer

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