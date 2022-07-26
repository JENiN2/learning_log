'''Определение ссхемы URL для learning_logs.'''
from django.urls import path

from . import views


urlpatterns = [
        # Домашняя страница
        path('', views.index, name='index'),
        # Вывод всех тем
        path('topics/', views.topics, name='topics'),
        # Страница с подробной информацией по отдельной теме
        path('topics/<topic_id>/', views.topic, name='topic'),
        # Удаляет тему
        path('delete_topic/<topic_id>', views.delete_topic, name='delete_topic'),
        # Страница для добавления новой темы
        path('new_topic/', views.new_topic, name='new_topic'),
        # Страница для добавления новой записи
        path('new_entry/<topic_id>/', views.new_entry, name='new_entry'),
        # страница для редактирования записи
        path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
        ]
