from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('weather_chatbot/', chatbot_view, name='weather_chatbot'),




]