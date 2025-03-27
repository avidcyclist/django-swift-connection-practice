from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player, Workout
from .serializers import PlayerSerializer, WorkoutSerializer

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