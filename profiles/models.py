from django.db import models

# Create your models here.

class Country(models.Model):

    country_name = models.CharField(max_length=255)

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=255)

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=255)