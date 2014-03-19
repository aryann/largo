from django.db import models


class Car(models.Model):
    vin = models.CharField(max_length=17, primary_key=True)
    name = models.CharField(max_length=16)
    city = models.CharField(max_length=16)

    def __repr__(self):
        return 'Car(vin={vin!r}, name={name!r}, city={city!r})'.format(
            vin=self.vin,
            name=self.name,
            city=self.city)

    def __unicode__(self):
        return repr(self)


class CollectionEventManager(models.Manager):
    
    def get_closest_event(self, time_sec):
        lt = self.filter(time_sec__lte=time_sec).order_by('-time_sec')
        gt = self.filter(time_sec__gte=time_sec).order_by('time_sec')

        print time_sec, lt, gt
        if lt and gt:
            print time_sec, lt[0].time_sec, gt[0].time_sec
            if time_sec - lt[0].time_sec < gt[0].time_sec - time_sec:
                return lt[0]
            else:
                return gt[0]
        elif lt:
            return lt[0]
        elif gt:
            return gt[0]
        else:
            raise self.model.DoesNotExist()


class CollectionEvent(models.Model):
    objects = CollectionEventManager()

    time_sec = models.FloatField()

    def __repr__(self):
        return 'CollectionEvent(time_sec={time_sec!r})'.format(
            time_sec=self.time_sec)

    def __unicode__(self):
        return repr(self)


class State(models.Model):
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lon = models.DecimalField(max_digits=10, decimal_places=5)
    event = models.ForeignKey('CollectionEvent')
    car = models.ForeignKey('Car')

    def __repr__(self):
        return ('State(lat={lat}, lon={lon}, event={event!r}, car={car!r})'
                .format(lat=self.lat,
                        lon=self.lon,
                        event=self.event,
                        car=self.car))

    def __unicode__(self):
        return repr(self)
