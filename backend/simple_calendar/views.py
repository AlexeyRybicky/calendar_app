"""Модуль содержит эндпоинты для приложения `simple_calendar`"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta

from simple_calendar.models import Event, Recurrence


# @api_view(['POST'])
# def add_event(request):
#     """
#     Добавляет событие
#     """
#
#     data = request.data
#     event = Event(
#         name=data['name'],
#         start_time=datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S'),
#         recurrence=data.get('recurrence')
#     )
#     event.save()
#
#     # Если указана периодичность, то создаем последовательность событий на год вперед
#     if event.recurrence:
#         recurrence_date = event.start_time.date()
#         while recurrence_date <= datetime.now().date() + timedelta(days=365):
#             RecurringEvent(event=event, recurrence_date=recurrence_date).save()
#             recurrence_date += timedelta(days=event.recurrence)
#
#     return Response({'id': event.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def add_event(request):
    """
    Добавляет событие
    """

    data = request.data
    event = Event.objects.create(
        name=data['name'],
        start_time=datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S'),
    )

    # Если указана периодичность, то создаем последовательность событий
    if 'period' in data and data['period'] is not None:
        Recurrence.objects.create(
            event=event,
            interval=data['period'],
            until=None
        )

    return Response({'id': event.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def remove_event(request, id, year, month, day):
    """
    Удаляет событие по id, оставляя все последующие
    """

    event_id = int(id)
    date = datetime(int(year), int(month), int(day)).date()

    event = get_object_or_404(Event, id=event_id)
    deleted_count, _ = RecurringEvent.objects.filter(event=event, recurrence_date=date).delete()

    return Response({'message': 'Событие удалено'}) if deleted_count > 0 else Response(
        {'message': 'Повторяющееся событие с указанной датой не найдено'},
        status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
def remove_next_events(request, id, year, month, day):
    """
    Удаляет событие и все последующие
    """

    event_id = int(id)
    date = datetime(int(year), int(month), int(day)).date()

    event = get_object_or_404(Event, id=event_id)
    deleted_count, _ = RecurringEvent.objects.filter(event=event, recurrence_date__gte=date).delete()

    return Response({'message': 'Все последующие события удалены'}) if deleted_count > 0 else Response(
        {'message': 'Не найдено событий для удаления'},
        status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
def update_event(request, id, year, month, day):
    """
    Обновляет имя события
    """

    event_id = int(id)
    date = datetime(int(year), int(month), int(day)).date()
    recurring_event = RecurringEvent.objects.get(event_id=event_id, recurrence_date=date)
    recurring_event.event.name = request.data['name']
    recurring_event.event.save()
    return Response({'message': 'Событие обновлено'})


@api_view(['GET'])
def get_events(request, year, month, day):
    """
    Показывает все события
    """

    date = datetime(int(year), int(month), int(day)).date()
    events = RecurringEvent.objects.filter(recurrence_date=date).select_related('event')
    result = [{'id': event.event.id, 'name': event.event.name} for event in events if not event.is_cancelled]
    return Response(result)
