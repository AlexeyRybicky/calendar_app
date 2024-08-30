"""Модуль содержит пути для приложения `simple_calendar`"""

from django.urls import path
from simple_calendar.views import add_event, remove_event, remove_next_events, update_event, get_events

urlpatterns = [
    path('add/', add_event, name='add_event'),
    path('remove/<int:id>/<int:year>/<int:month>/<int:day>/', remove_event, name='remove_event'),
    path('remove-next/<int:id>/<int:year>/<int:month>/<int:day>/', remove_next_events, name='remove_next_events'),
    path('update/<int:id>/<int:year>/<int:month>/<int:day>/', update_event, name='update_event'),
    path('events/<int:year>/<int:month>/<int:day>/', get_events, name='get_events'),
]
