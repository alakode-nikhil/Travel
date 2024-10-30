from django import forms
from .models import *

class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = '__all__'
        widgets = {
            'place_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Destination'}),
            'weather': forms.Select(attrs={'class':'form-control','placeholder':'Enter the author'}),
            'state': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the State'}),
            'district': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the District'}),
            'map_url': forms.URLInput(attrs={'class':'form-control','placeholder':'Enter the map link'}),
            'description': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Description'}),
        }