from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'largo.views.index'),
    url(r'^getcars/(?P<time>\d+)$', 'largo.views.get_cars'),
)
