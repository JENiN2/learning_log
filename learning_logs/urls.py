'''Определение ссхемы URL для learning_logs.'''
from django.urls import path

from . import views


urlpatterns = [
        # Домашняя страница
        path('', views.index, name='index')
]
