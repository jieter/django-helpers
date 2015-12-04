import json

from django.test import SimpleTestCase

from helpers.containers import TimeseriesContainer
from helpers.http import JSON_DATETIME_FORMAT, json_response
from helpers.time import (Extents, local_datetime, local_timezone,
                          parse_utc_datetime)


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

    def test_list(self):
        l = ['foo', 'bar', 1]
        response = json_response(l)

        response_json = json.loads(response.content)

        self.assertEqual(response_json, l)

    def test_extents(self):
        e = Extents(period='year')
        response = json_response(e)
        response_json = json.loads(response.content)

        start, end = e
        self.assertEquals(
            parse_utc_datetime(response_json[0], JSON_DATETIME_FORMAT).year,
            start.year
        )

    def test_timeseriescontainer(self):
        keys = ['timestamp', 'foo']
        values = (
            (local_datetime(2015, 1, 1, 12, 0, 0), 1),
            (local_datetime(2015, 1, 2, 12, 0, 0), 2),
            (local_datetime(2015, 1, 3, 12, 0, 0), 3),
            (local_datetime(2015, 1, 4, 12, 0, 0), 4)
        )
        container = TimeseriesContainer(keys, values)

        response = json_response(container)
        # is valid json
        response_json = json.loads(response.content)

        self.assertEquals(response_json['keys'], keys)
