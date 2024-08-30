"""В моделу содержиться модель базы данных приложения `simple_calendar`"""

from django.db import models


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

    def __str__(self):
        """Возвращает имя события"""
        return self.name


class Recurrence(models.Model):
    """Модель для повторяющихся событий"""

    objects: models.Manager

    # class Frequency(models.TextChoices):
    #     DAILY = 'daily', 'Daily'
    #     WEEKLY = 'weekly', 'Weekly'
    #     MONTHLY = 'monthly', 'Monthly'

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='recurrence'
    )
    # frequency = models.CharField(
    #     max_length=50,
    #     choices=Frequency.choices,
    #     help_text="Частота повторения"
    # )
    interval = models.PositiveIntegerField(
        default=1,
        help_text="Интервал повторения"
    )
    until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Дата окончания повторений"
    )

    def __str__(self):
        """Возвращает параметры повторения"""
        return f"{self.event.name} - повторяется каждые {self.interval}"
