import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

JSON_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
try:
    DEBUG = settings.DEBUG
except:
    DEBUG = True


def json_handler(obj):
    if isinstance(obj, datetime):
        return obj.strftime(JSON_DATETIME_FORMAT)
    elif hasattr(obj, 'to_json_dict'):
        return obj.to_json_dict()
    else:
        return list(obj)


dumpkwargs = {
    'default': json_handler,
    'indent': 2 if DEBUG else None,
    'separators': (', ', ': ') if DEBUG else (',', ':'),
}


def json_response(data):
    '''Wrap to json converted python structures in an HttpResponse and add json content type'''

    return HttpResponse(json.dumps(data, **dumpkwargs), content_type='application/json')
