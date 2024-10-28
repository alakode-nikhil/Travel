from .models import *
from rest_framework import serializers

class DestinationSerializer(serializers.ModelSerializer):

    img  = serializers.ImageField(required = False)
 
    class Meta:
        model = Destination
        fields = '__all__'