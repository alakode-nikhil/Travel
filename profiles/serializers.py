from .models import *
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'

    def validate_country(self, value):
        if not Country.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('Country not found')
        return value

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

    def validate_state(self, value):
        if not State.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('State not found')
        return value