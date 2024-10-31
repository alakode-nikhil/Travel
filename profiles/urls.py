from django.urls import path
from .views import *

urlpatterns = [
    path('api/create-country/', CreateCountryApi.as_view(), name='api-create-country'),
    path('api/create-state/', CreateStateApi.as_view(), name='api-create-state'),
    path('api/create-district/', CreateDistrictApi.as_view(), name='api-create-district'),
]