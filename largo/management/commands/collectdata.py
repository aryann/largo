import os
import requests
import time

from django.core.management import base
from largo import models

URL = 'https://www.car2go.com/api/v2.1/vehicles'
CITY = 'seattle'


class Command(base.BaseCommand):
    
    help = 'Performs a single collection of data.'

    def handle(self, *args, **options):
        collection_event = models.CollectionEvent(time_sec=time.time())
        collection_event.save()

        res = requests.get(URL, params={
                'loc': CITY,
                'oauth_consumer_key': 'car2gowebsite',
                'format': 'json',
                })
        for car in res.json()['placemarks']:
            coords = car['coordinates']
            car_obj, _ = models.Car.objects.get_or_create(
                vin=car['vin'],
                name=car['name'],
                city=CITY)
            state = models.State(
                lat=coords[0],
                lon=coords[1],
                event=collection_event,
                car=car_obj)
            self.stderr.write('Saving state: {0}'.format(state))
            state.save()
