from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Country(models.Model):

    country_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.country_name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.state_name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.district_name
    
class Porfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)