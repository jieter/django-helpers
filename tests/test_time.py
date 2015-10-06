from datetime import datetime

from django.test import SimpleTestCase
from django.utils.timezone import utc
from helpers.time import (date_equals, local_datetime, parse_utc_datetime,
                          quarter, round_to_interval, round_to_minute)


class TestLocalDatetime(SimpleTestCase):
    # Europe/Amsterdam is assumed
    def test_utc_vs_amsterdam(self):
        t = datetime(2015, 6, 18, 12, 0, 0, tzinfo=utc)
        self.assertEquals(t, local_datetime(2015, 6, 18, 14, 0, 0))

    def test_amsterdam_vs_utc(self):
        t = local_datetime(2015, 6, 18, 14, 0, 0)
        self.assertEquals(t, datetime(2015, 6, 18, 12, 0, 0, tzinfo=utc))

    def test_without_DST(self):
        t = datetime(2015, 1, 18, 12, 0, 0, tzinfo=utc)
        self.assertEquals(t, local_datetime(2015, 1, 18, 13, 0, 0))


class test_dateEquals(SimpleTestCase):
    def test_date_equals(self):
        date_is_equal = (
            (
                datetime(2015, 1, 18, 12, 0, 0, tzinfo=utc),
                datetime(2015, 1, 18, 13, 0, 0, tzinfo=utc)
            ),
            (
                datetime(2015, 1, 18, 12, 0, 0, tzinfo=utc),
                datetime(2015, 1, 18, 23, 0, 0, tzinfo=utc)
            ),
            (
                datetime(2015, 1, 18, 12, 0, 0, tzinfo=utc),
                datetime(2015, 1, 18, 13, 0, 0)
            ),
        )

        date_is_not_equal = (
            (
                datetime(2016, 1, 18, 12, 0, 0, tzinfo=utc),
                datetime(2015, 1, 18, 13, 0, 0, tzinfo=utc)
            ),
            (
                datetime(2016, 1, 18, 12, 0, 0, tzinfo=utc),
                datetime(2015, 1, 18, 13, 0, 0)
            ),
        )
        for a, b in date_is_equal:
            self.assertTrue(date_equals(a, b))

        for a, b in date_is_not_equal:
            self.assertFalse(date_equals(a, b))


class TimestampRounding(SimpleTestCase):

    def test_round_to_minute(self):
        tests = (
            (
                datetime(2014, 1, 1, 11, 11, 11),
                datetime(2014, 1, 1, 11, 11, 0)
            ), (
                datetime(2014, 6, 18, 12, 25, 59),
                datetime(2014, 6, 18, 12, 25, 00),
            ), (
                datetime(1999, 6, 6, 12, 25, 00),
                datetime(1999, 6, 6, 12, 25, 00),
            )
        )

        for test, expected in tests:
            self.assertEqual(round_to_minute(test), expected)

    def test_parsed(self):
        '''
        Test with a couple of timestamps from a real log
        '''
        with open('tests/fixtures/timestamps.txt', 'r') as stamps:
            for line in stamps:
                t = parse_utc_datetime(line.strip())
                t = round_to_minute(t)

                self.assertEqual(t.second, 0)

    def test_round_to_hour(self):
        tests = (
            (
                datetime(2014, 1, 1, 11, 11, 11),
                datetime(2014, 1, 1, 11, 0, 0)
            ), (
                datetime(2014, 6, 18, 12, 25, 59),
                datetime(2014, 6, 18, 12, 0, 0),
            )
        )
        for test, expected in tests:
            self.assertEqual(round_to_interval(test, 'hour'), expected)

    def test_round_to_day(self):
        tests = (
            (
                datetime(2014, 1, 1, 11, 11, 11),
                datetime(2014, 1, 1, 0, 0, 0)
            ), (
                datetime(2014, 6, 18, 12, 25, 59),
                datetime(2014, 6, 18, 0, 0, 0),
            )
        )
        for test, expected in tests:
            self.assertEqual(round_to_interval(test, 'day'), expected)

    def test_round_to__multiple(self):
        t = datetime(2014, 1, 1, 11, 11, 11)
        self.assertEqual(round_to_interval(t, 'hour', 2), datetime(2014, 1, 1, 10, 0, 0))
        self.assertEqual(round_to_interval(t, 'minute', 15), datetime(2014, 1, 1, 11, 0, 0))
        self.assertEqual(round_to_interval(t, 'minute', 5), datetime(2014, 1, 1, 11, 10, 0))
        self.assertEqual(round_to_interval(t, 'minute', 10), datetime(2014, 1, 1, 11, 10, 0))

    def test_round_to_interval_years(self):
        def raises():
            t = datetime(2014, 1, 1, 11, 11, 11)
            return round_to_interval(t, 'year')

        self.assertRaises(ValueError, raises)


class TestQuarter(SimpleTestCase):
    def test_invalid(self):
        self.assertRaises(ValueError, lambda: quarter(2015, 6))

    def test_valid(self):
        tests = (
            (quarter(2014, 1), (2014, 1, 1), (2014, 3, 31)),
            (quarter(2001, 2), (2001, 4, 1), (2001, 6, 30)),
            (quarter(2015, 3), (2015, 7, 1), (2015, 9, 30)),
            (quarter(2016, 4), (2016, 10, 1), (2016, 12, 31)),
        )
        for actual, start, end in tests:
            start = local_datetime(start)
            end = local_datetime(end)
            self.assertEqual(actual[0], start)
            self.assertEqual(actual[1], end)
