import json
import time

from django import http
from django import shortcuts
from largo import models


def index(request):
    context = {'time_sec': time.time()}
    return shortcuts.render(
        request, 'largo/index.html', context)


def get_cars(request):
    time_sec = float(request.GET.get('time_sec', time.time()))
    try:
        collection_event = (
            models.CollectionEvent.objects.get_closest_event(time_sec))
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
