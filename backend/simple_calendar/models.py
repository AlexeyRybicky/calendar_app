"""В моделу содержиться модель базы данных приложения `simple_calendar`"""

from django.db import models
from django.utils import timezone


class Event(models.Model):
    """Модель `Event` содержит информацию о событиях"""

    objects: models.Manager

    name = models.CharField(
        max_length=255,
        help_text="Название события"
    )
    start_time = models.DateTimeField(
        help_text="Дата начанала события"
    )
    recurrence = models.IntegerField(
        null=True,
        blank=True,
        help_text="Периодичность повторения"
    )

    def __str__(self):
        """Возвращает имя события"""
        return self.name


class RecurringEvent(models.Model):
    """Модель для повторяющихся событий"""

    objects: models.Manager

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='recurring_events'
    )
    recurrence_date = models.DateField(
        help_text='Дата повторения'
    )
    is_cancelled = models.BooleanField(
        default=False,
        help_text='Фалг отмены события'
    )

    def __str__(self):
        """Возвращает даты повторения у события"""
        return f"{self.event.name} - {self.recurrence_date}"

    class Meta:
        unique_together = ('event', 'recurrence_date')
