from collections import defaultdict

from django.db import connection, models

from .time import is_interval_valid, parse_interval, round_to_interval


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created', )
        get_latest_by = 'created'


class AggregationMixin(object):
    def group_by_interval(self, *args, **kwargs):
        return group_by_interval(self, *args, **kwargs)


def prefix(s):
    return '_%s' % s


def avg(lst):
    '''Return the average (mean) of a list'''
    return sum(lst) / float(len(lst))


def group_by_interval(queryset, interval, aggregates, field_name='timestamp'):
    # drew some inspiration for this function from:
    # https://bitbucket.org/kmike/django-qsstats-magic
    num, interval = parse_interval(interval)

    if interval not in ('minute', 'hour', 'day', 'month', 'year'):
        raise ValueError('Interval (%s) not supported by date_trunc()' % interval)

    label = prefix(field_name)

    lookup = {
        'max': models.Max,
        'min': models.Min,
        'avg': models.Avg,
        'sum': models.Sum,
        'count': models.Count
    }
    aggregates_dict = {prefix(key): lookup[function](key) for key, function in aggregates}

    # this is not really a public API but much more portable than using
    # raw date_trunc in extra().
    aggregator = connection.ops.date_trunc_sql(interval, field_name)

    prefixed_keys = [label, ] + map(prefix, [a[0] for a in aggregates])

    # explicit order_by() call required to cancel effect of default ordering on models
    values = queryset \
        .extra({label: aggregator}) \
        .values(label) \
        .order_by() \
        .annotate(**aggregates_dict) \
        .order_by(label) \
        .values_list(*prefixed_keys)

    if num == 1:
        return values
    else:
        return _group_by_multiple(values, num, interval, aggregates=[a[1] for a in aggregates])


def _group_by_multiple(values, num, interval, aggregates=('sum', )):
    if values is None or len(values) == 0:
        return values

    assert is_interval_valid(interval), 'Interval should be valid'
    assert len(values[0]) == 1 + len(aggregates), \
        'Number of items in each row does not agree with number of aggregates'

    aggregated = defaultdict(lambda: [0] * len(aggregates))

    for row in values:
        timestamp = round_to_interval(row[0], interval, num)
        for key, aggregate in enumerate(aggregates):
            value = row[key + 1]
            if aggregate in ('sum', 'count'):
                aggregated[timestamp][key] += value

            elif aggregate == 'avg':
                if aggregated[timestamp][key] == 0:
                    aggregated[timestamp][key] = []
                aggregated[timestamp][key].append(value)

            elif aggregate == 'max':
                aggregated[timestamp][key] = max(aggregated[timestamp][key], value)

            else:
                raise ValueError('No such aggregate defined')

    # We need to do the averaging
    items = [
        (t, ) + tuple(avg(f) if isinstance(f, list) else f for f in fields)
        for t, fields in aggregated.items()
    ]

    return sorted(items, key=lambda x: x[0])
