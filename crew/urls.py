from django.urls import path
from .views import CrewJoin

urlpatterns = [
    path("join/", CrewJoin.as_view(), name='join'),
]
