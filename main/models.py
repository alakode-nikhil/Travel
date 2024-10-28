from django.db import models

# Create your models here.

class Destination(models.Model):
    place_name = models.CharField(max_length=250)
    WEATHER_CHOICES = [
        (1, 'Sunny'),
        (2,'Rainy'),
        (3,'Clody'),
        (4,'Foggy'),
        (5,'Snowy'),
        (6,'Windy')
    ]
    weather = models.IntegerField(choices=WEATHER_CHOICES)
    img = models.ImageField(upload_to='recipes/')
    state = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    map_url = models.URLField(max_length=2000, blank=True)
    description = models.TextField()

