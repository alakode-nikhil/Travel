from django.urls import path
from .views import *

urlpatterns = [
   path('api/create-destination/', CreateDestinationApi.as_view(), name='api-create-destination'),
    path('api/list-destination/<int:pk>/', ListDestinationApi.as_view(), name='api-list-destination'),
    path('api/update-destination/<int:pk>/', UpdateDestinationApi.as_view(), name='api-update-destination'),
    path('api/delete-destination/<int:pk>/', DeleteDestinationApi.as_view(), name='api-delete-destination'),
    path('api/search-destination/<str:name>/', SearchDestinationApi.as_view(), name='api-search_destination'),  
]