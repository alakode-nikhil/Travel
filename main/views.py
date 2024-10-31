from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import requests
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .forms import *

# Create your views here.

class CreateDestinationApi(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ListDestinationApi(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UpdateDestinationApi(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

class DeleteDestinationApi(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

class SearchDestinationApi(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

        api_url = f'http://127.0.0.1:8000/api/search-destination/{search}/'

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

                paginator = Paginator(original_data, 9)
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

def update_destination(request, id):
    info_url = f'http://127.0.0.1:8000/api/list-destination/{id}/'
    response = requests.get(info_url)
    destination = response.json()
    if request.method == 'POST':
        place_name = request.POST['place_name']
        state = request.POST['state']
        district = request.POST['district']
        weather = request.POST['weather']
        map_url = request.POST['map_url']
        description = request.POST['description']
        api_url = f'http://127.0.0.1:8000/api/update-destination/{id}/'
        print(response.status_code)

        data = {
            'place_name': place_name,
            'state': state,
            'district': district,
            'weather': weather,
            'map_url':map_url,
            'description': description
        }

        files = {'img': request.FILES.get('img')}
        response = requests.put(api_url, data = data, files = files)

        if response.status_code == 200:
            messages.success(request, 'Destination updated')
            return redirect('/')
        
        elif response.status_code == 403:
            messages.info(request, 'You are not logged in, Please log in')
            return redirect('login')
        
        else:
            messages.error(request, f'Error submitting data to the REST API {response.status_code}')

    return render(request, 'update-destination.html', {'destination':destination})

def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/api/create-destination/'
                data = form.cleaned_data

                response = requests.post(api_url, data=data, files = {'img': request.FILES['img']})

                if response.status_code == 400:
                    messages.success(request, 'Destination Inserted Successfully!')
                    return redirect('/')
                
                elif response.status_code == 403:
                    messages.info(request, 'You are not logged in, Please log in')
                    return redirect('login')
                
                else:
                    messages.error(request, f'Error{response.status_code}')

            except requests.RequestException as e:
                messages.error(request, f'Error during API request {str(e)}')

        else:
            messages.error(request, 'Invalid Form')

    else:
        form = DestinationForm
        
    return render(request, 'create-destination.html', {'form': form})

def delete_destination(request, id):

    api_url = f'http://127.0.0.1:8000/api/delete-destination/{id}/'
    response = requests.delete(api_url)

    if response.status_code == 200:
        print(f'Item with id {id} successfully deleted')

    elif response.status_code == 403:
            messages.info(request, 'You are not logged in, Please log in')
            return redirect('login')

    else:
        print(f'Fail to delete item {id} {response.status_code}')

    return redirect('/')
