import logging

from django.conf import settings
from django.db import models

from geopy.geocoders import Nominatim

from .exception import exception_message

logger = logging.getLogger('helpers.geo')


def geocoder(string):
    if settings.TEST_MODE:
        return None
    try:  # pragma: no cover
        geocoder = Nominatim(country_bias='NL', timeout=0.5)
        return geocoder.geocode(str(string))
    except Exception:  # pragma: no cover
        logger.debug(exception_message())
        return None


class GeoLocationMixin(models.Model):

    lat = models.FloatField(editable=False, null=True)
    lng = models.FloatField(editable=False, null=True)

    STATUS_PENDING = 'pending'
    STATUS_ERROR = 'error'
    STATUS_SUCCESS = 'success'
    GEOCODE_STATUS_CHOICES = (
        (STATUS_PENDING, 'Not yet geocoded'),
        (STATUS_ERROR, 'Geocoder returned error'),
        (STATUS_SUCCESS, 'Succesfully geocoded')
    )
    geocode_status = models.CharField(
        max_length=15,
        choices=GEOCODE_STATUS_CHOICES,
        editable=False,
        default=STATUS_PENDING
    )

    class Meta:
        abstract = True

    def geo_get_address(self):
        '''By default, just cast self to string'''
        return str(self)

    def is_geocoded(self):
        return self.geocode_status == self.STATUS_SUCCESS

    def has_location(self):
        if self.is_geocoded():
            return True

        if self.geocode_status in (self.STATUS_PENDING, ):
            self.geocode()

        return self.geocode_status == self.STATUS_SUCCESS

    def get_location(self):
        return (self.lat, self.lng)

    def geocode(self):
        location = geocoder(self.geo_get_address())
        if location is None or not location.latitude:
            self.geocode_status = self.STATUS_ERROR
        else:
            self.lat, self.lng = (location.latitude, location.longitude)
            self.geocode_status = self.STATUS_SUCCESS

        self.save()

    def debug_location(self):
        self.geocode()
        if self.is_geocoded():
            return self.geocode_status + ': %f, %f' % self.get_location()

        else:
            return self.geocode_status
