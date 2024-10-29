from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class CreateDestinationApi(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]

class ListDestinationApi(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class UpdateDestinationApi(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DeleteDestinationApi(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class SearchDestinationApi(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        name = self.kwargs.get('name')
        if name:
            return Destination.objects.filter(place_name__icontains = name)
        
        return Destination.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No destinations found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)