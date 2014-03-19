import json

from django import http
from largo import models


def index(request):
    return http.HttpResponse('Hello world!\n')


def get_cars(request, time):
    try:
        collection_event = (
            models.CollectionEvent.objects.get_closest_event(float(time)))
    except models.CollectionEvent.DoesNotExist:
        return http.HttpResponse('[]')

    states = models.State.objects.filter(
        event=collection_event).select_related('car')
    res = []
    for state in states:
        res.append({
                'lat': float(state.lat),
                'lon': float(state.lon),
                'name': state.car.name,
                })

    return http.HttpResponse(json.dumps(res))
