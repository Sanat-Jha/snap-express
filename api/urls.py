from django.urls import path
from .views import *
urlpatterns = [
    # path('face-swap',swapface,name='swapface'),
    path('swapface',swapface,name='swapface'),
]
