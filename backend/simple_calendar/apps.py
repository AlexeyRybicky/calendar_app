"""Модуль содержит базовую конфигурацию приложения `simple_calendar`"""

from django.apps import AppConfig


class SimpleCalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_calendar'
