import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

from .containers import TimeseriesContainer
from .time import Extents

JSON_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def handler(obj):
    if isinstance(obj, datetime):
        return obj.strftime(JSON_DATETIME_FORMAT)
    elif isinstance(obj, Extents):
        return list(obj)
    elif isinstance(obj, TimeseriesContainer):
        return obj.to_json_dict()
    else:
        raise TypeError

dumpkwargs = {
    'default': handler,
    'indent': 2 if settings.DEBUG else None,
    'separators': (', ', ': ') if settings.DEBUG else (',', ':'),
}


def json_response(data):
    '''Wrap to json converted python structures in an HttpResponse and add json content type'''

    return HttpResponse(json.dumps(data, **dumpkwargs), content_type='application/json')
