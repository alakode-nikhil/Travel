from django.urls import path
from .views import *

urlpatterns = [
    path('api/create-country/', CreateCountryApi.as_view(), name='api-create-country'),
    path('api/create-state/', CreateStateApi.as_view(), name='api-create-state'),
    path('api/create-district/', CreateDistrictApi.as_view(), name='api-create-district'),
    path('api/states/<int:country_id>/', StateByCountryApi.as_view(), name='states-by-country'),
    path('api/districts/<int:state_id>/', DistrictByStateApi.as_view(), name='districts-by-state'),
]