from datetime import datetime

from .time import local_timezone


class TimeseriesContainer(object):

    def __init__(self, keys, values, **kwargs):
        if len(values) > 0 and len(keys) != len(values[0]):
            raise ValueError('Number of keys does not equal number of values in first item')

        self.keys = list(keys)
        self.values = list(values)

        self.extra = kwargs

    def _item(self, item):
        return dict(zip(self.keys, item))

    def __getitem__(self, item):
        if item > len(self.values):
            raise IndexError
        else:
            return self._item(self.values[item])

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        for v in self.values:
            yield self._item(v)

    def sum(self, key):
        idx = self.keys.index(key)
        return sum(v[idx] for v in self.values)

    def prepare_for_view(self, timezone=local_timezone, float_precision=2):
        def transform(val):
            if isinstance(val, datetime):
                return timezone.normalize(val)
            elif isinstance(val, float):
                return round(val, float_precision)
            else:
                return val

        self.values = [map(transform, x) for x in self.values]

    def to_json_dict(self, **kwargs):
        self.prepare_for_view()
        data = {
            'keys': self.keys,
            'values': self.values,
        }
        data.update(self.extra)
        data.update(kwargs)
        return data
