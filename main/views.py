from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import requests
from django.core.paginator import Paginator, EmptyPage, InvalidPage

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
    
def index(request):

    if request.method =='POST':
        search = request.POST['search']

        api_url = f'http:127.0.0.1:8000/api/search-destination/{search}/'

        try:
            response = requests.get(api_url)
            print(response.status_code)

            if response.status_code == 200:
                data = response.json()

            else:
                data = None

        except requests.RequestException as e:
            data = None

        return render(request, 'index.html', {'data':data})
    
    else:

        api_url = 'http://127.0.0.1:8000/api/create-destination/'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                original_data = data

                paginator = Paginator(original_data, 10)
                page = request.GET.get('page', 1)

                try:
                    destinations = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    destinations = paginator.page(paginator.num_pages)

                context = {
                    'original_data': original_data,
                    'destinations': destinations
                }

                return render(request, 'index.html', context)
            
            else:

                return render(request, 'index.html', {'error_message':f'Error {response.status_code}' })
        
        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message':f'Error {e}'})
        
def fetch_destination(request, id):

    api_url = f'http://127.0.0.1:8000/api/list-destination/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        data['weather_display'] = get_weather_display(data.get('weather'))
        return render(request, 'fetch-destination.html', {'destination':data})
    
    return render(request,'fetch_destination.html')

#Convert Weather code to human understandable text!
def get_weather_display(weather_code):
    WEATHER_CHOICES = {
        1: 'Sunny',
        2: 'Rainy',
        3: 'Cloudy',
        4: 'Foggy',
        5: 'Snowy',
        6: 'Windy'
    }
    return WEATHER_CHOICES.get(weather_code, "Unknown")