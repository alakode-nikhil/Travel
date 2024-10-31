from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests

# Create your views here.
class CreateCountryApi(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CreateStateApi(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class CreateDistrictApi(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]

#Fetch APIs for dependent dropdown
class StateByCountryApi(generics.ListAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        country_id = self.kwargs['country_id']
        return State.objects.filter(country_id=country_id)

class DistrictByStateApi(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        return District.objects.filter(state_id=state_id)
    
#Fetch API end

def register_user(request):

    country_url = f'http://127.0.0.1:8000/profiles/api/create-country/'
    country_response = requests.get(country_url)
    countries = country_response.json()
    if request.method =='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country_id = request.POST.get('country')
        country = Country.objects.get(id = country_id)
        state_id = request.POST.get('state')
        state = State.objects.get(id= state_id)
        district_id = request.POST.get('district')
        district = District.objects.get(id = district_id)
        password = request.POST.get('pass')
        cpass = request.POST.get('cpass')

        if cpass != password:
            messages.info(request,'Password mismatch')
            return redirect('register')
        
        if User.objects.filter(username = username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.info(request,'Email already exists')
            return redirect('register')
        user = User.objects.create_user(username=username, first_name= first_name, last_name = last_name, password= password, email=email)
        user.save()
        profile = Profile.objects.create(user = user, country = country, state = state, district = district)
        profile.save()
        return redirect('login')
    
    return render(request, 'register.html', {'countries':countries})

def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password= password)
        try:          
            login(request,user)
            return redirect('home-destination')
        except:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    
    return render(request,'login.html')

def logout_user(request):

    logout(request)
    return redirect('home-destination')
