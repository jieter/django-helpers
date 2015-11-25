import re
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.utils.timezone import get_default_timezone, now
from isoweek import Week

local_timezone = get_default_timezone()

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def local_datetime(*args):
    '''Compose a datetime object of the arglist and localize it to the local timezone'''
    if len(args) == 1:
        t = args[0] if isinstance(args[0], datetime) else datetime(*args[0])
    else:
        t = datetime(*args)

    return local_timezone.localize(t)


def round_to_interval(t, interval, num=1):
    if interval == 'minute':
        diff = timedelta(minutes=t.minute % num)
    elif interval == 'hour':
        diff = timedelta(
            hours=t.hour % num,
            minutes=t.minute
        )
    elif interval == 'day':
        diff = timedelta(
            days=t.day % num,
            hours=t.hour,
            minutes=t.minute
        )
    else:
        raise ValueError('Not defined for interval: %s' % interval)

    return t - diff - timedelta(seconds=t.second, microseconds=t.microsecond)


def round_to_minute(t, minute=1):
    '''Round a timestamp to a fixed number of minutes, which is one by default.
    Removes the seconds/microseconds and rounds the number of minutes to the
    closest multiple of `minute` argument'''

    return round_to_interval(t, 'minute', minute)


def parse_interval(interval):
    match = re.match('(\d+)([A-Za-z]+)', interval)

    if match:
        return int(match.group(1)), match.group(2)
    else:
        return 1, interval


def is_interval_valid(interval):
    num, period = parse_interval(interval)
    VALID = ('minute', 'hour', 'day', 'month', 'year')

    return period in VALID


def readable_interval(interval):
    num, interval = parse_interval(interval)

    # TODO: fix this with proper i18n / humanize
    mapping = dict(
        year=('jaar', 'jaren'),
        month=('maand', 'maanden'),
        week=('week', 'weken'),
        day=('dag', 'dagen'),
        hour=('uur', 'uren'),
        minute=('minuut', 'minuten'),
        second=('seconde', 'seconden'),
    )
    if num == 1:
        return mapping[interval][0]
    else:
        return '%d %s' % (num, mapping[interval][1])


def parse_utc_datetime(instring, fmt=DATETIME_FORMAT):
    '''Parse a datetime string and localize to UTC'''
    timestamp = datetime.strptime(instring, fmt)

    return pytz.utc.localize(timestamp)


def date_equals(a, b):
    '''return true if the date parts of two datetime strings are equal.'''
    return a.date() == b.date()


def clean_day(t):
    '''Set everything less significant than day to 0'''
    return t.replace(hour=0, minute=0, second=0, microsecond=0)


def clean_month(t):
    '''Set day to 1 and everything less significant to 0'''
    return clean_day(t).replace(day=1)


def clean_year(t):
    '''Set day and month to 1 and everything less significant to 0'''
    return clean_month(t).replace(month=1)


class Extents(object):
    '''
    Represents the start and end of a period around a point in time t.

    Possible periods are: day, week, month, year
    '''
    VALID_PERIODS = ('year', 'month', 'week', 'day', None)

    # Interesting stackoverflow question about timezones, DST etc:
    # http://stackoverflow.com/questions/2532729/daylight-saving-time-and-time-zone-best-practices
    def __init__(self, timestamp=None, period=None):
        if timestamp is None:
            timestamp = now()
        if timestamp.tzinfo is None:
            raise ValueError('You cannot pass naive timestamp to Extent')
        self.timestamp = local_timezone.normalize(timestamp)

        self.set_period(period)

    def __str__(self):
        t = self.timestamp.__repr__()
        if self.period is None:
            return 'Extents for undefined period around %s' % t
        else:
            return 'Extents for `%s` around %s' % (self.period, t)

    def set_period(self, period):
        if not self.is_valid_period(period):
            raise ValueError('Period "%s" is not a valid period' % period)
        self.period = period

    def for_period(self, period):
        '''Return a clone with the period defined'''
        return Extents(self.timestamp, period)

    def is_valid_period(self, period):
        return period in self.VALID_PERIODS

    def __iter__(self):
        return iter(self.to_tuple())

    def __getitem__(self, key):
        return self.to_tuple()[key]

    def to_tuple(self):
        if self.period is not None:
            return getattr(self, self.period)()
        else:
            raise ValueError('Period must be defined')

    def slices(self, interval):
        start, end = self
        span = (end - start).total_seconds() + 1

        num, interval = parse_interval(interval)

        if interval == 'minute':
            ret = span / (num * 60)
        elif interval == 'hour':
            ret = span / (num * 60 * 60)
        elif interval == 'day':
            ret = span / (num * 24 * 60 * 60)
        else:
            raise ValueError('Not yet supported interval: %s' % interval)

        return int(ret)

    def slice(self, size=None):
        '''
        Generate slices of the current time extent,
        size in seconds or a timedelta object.
        TODO: use same interval praram as slices method.
        '''
        start, end = self
        if size is None:
            size = timedelta(seconds=5)
        elif isinstance(size, (int, float)):
            size = timedelta(seconds=size)

        current = start
        while current < end:
            yield current
            current += size

    def current(self):
        return self.timestamp

    def previous(self):
        start, end = self.to_tuple()
        return clean_day(start - (end - start) / 2)

    def next(self):
        start, end = self.to_tuple()
        return clean_day(end + (end - start) / 2)

    def day(self):
        'Returns the start, end-tuple for a day around self.timestamp'
        start = clean_day(self.timestamp)
        end = start + timedelta(hours=23, minutes=59, seconds=59)

        return (start, end)

    def week(self):
        'Returns the start, end-tuple for a week around self.timestamp'
        w = Week.withdate(self.timestamp)
        start = clean_day(local_timezone.localize(datetime.combine(w.monday(), datetime.min.time())))
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        return (start, end)

    def month(self):
        'Returns the start, end-tuple for a month around self.timestamp'
        start = clean_month(self.timestamp)
        end = start + relativedelta(months=1) - timedelta(seconds=1)

        return (start, end)

    def year(self):
        'Returns the start, end-tuple for a year around self.timestamp'
        start = clean_year(self.timestamp)
        end = start.replace(year=start.year + 1) - timedelta(seconds=1)

        return (start, end)


def quarter(year, q):
    'returns the start and end of a quarter'
    start_months = (1, 4, 7, 10)
    q = int(q)
    if q not in (1, 2, 3, 4):
        raise ValueError('Quarter should be a number from 1 to 4')

    start = datetime(int(year), start_months[q - 1], 1, 0, 0, 0)
    end = start + relativedelta(months=3) - relativedelta(days=1)
    return (
        local_timezone.localize(start),
        local_timezone.localize(end)
    )
