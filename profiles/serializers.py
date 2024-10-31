from .models import *
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):

    country = CountrySerializer()
    class Meta:
        model = State
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):

    state = StateSerializer()
    class Meta:
        model = State
        fields = '__all__'