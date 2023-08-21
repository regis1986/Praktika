from django.urls import path
from . import views

urlpatterns = [
    path('auto', views.index, name='index'),
    ]