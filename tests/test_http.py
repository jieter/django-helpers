import json

from django.test import SimpleTestCase

from helpers.http import JSON_DATETIME_FORMAT, json_response
from helpers.time import local_timezone, parse_utc_datetime


class Obj(object):
    foo = 'bar'
    bar = 'foo'


class JsonResponseTest(SimpleTestCase):

    def test_transformation(self):
        dt = parse_utc_datetime('2014-04-16 12:12:12')
        indata = dict(timestamp=dt)

        response = json_response(indata)
        outdata = json.loads(response.content)

        self.assertEquals(
            parse_utc_datetime(outdata['timestamp'], JSON_DATETIME_FORMAT),
            indata['timestamp'].astimezone(local_timezone)
        )

    def test_object_raises(self):
        data = {
            'foo': Obj()
        }

        self.assertRaises(TypeError, json_response, data)
