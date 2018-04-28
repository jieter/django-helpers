from datetime import datetime

from django.test import SimpleTestCase
from django.utils.timezone import utc

from helpers.time import Extents, local_datetime


class ExtentsTest(SimpleTestCase):
    def assert_extents(self, extents, start, end):
        message = '%s of extents not equal: \nactual: %s\nexpect: %s'
        actual_start, actual_end = extents

        expect = local_datetime(*start)
        self.assertEqual(actual_start, expect, message % (
            'start',
            actual_start.__repr__(),
            expect.__repr__()
        ))

        expect = local_datetime(*end)
        self.assertEqual(actual_end, expect, message % (
            'end',
            actual_end.__repr__(),
            expect.__repr__()
        ))

    def test_to_tuple(self):
        extents = Extents(period='day')
        extents_tuple = tuple(extents)

        self.assertEqual(extents_tuple, extents.to_tuple())
        self.assertEqual(extents_tuple[0], extents[0])
        self.assertEqual(extents_tuple[1], extents[1])

    def test_extents_naive(self):
        self.assertRaises(ValueError, lambda: Extents(datetime(2015, 1, 4)))

    def test_extents_day(self):
        t = local_datetime(2014, 6, 18, 11, 11, 11)
        extents = Extents(t, 'day')

        self.assertEqual(t, extents.current())
        self.assert_extents(extents, (2014, 6, 18, 0, 0, 0), (2014, 6, 18, 23, 59, 59))

    def test_extents_week(self):
        # monday june 16 ... sunday june 22
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), 'week')

        self.assert_extents(extents, (2014, 6, 16, 0, 0, 0), (2014, 6, 22, 23, 59, 59))

    def test_extents_month(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), 'month')

        self.assert_extents(extents, (2014, 6, 1, 0, 0, 0), (2014, 6, 30, 23, 59, 59))

        # # this fails around DST switch on 28 march 2015
        # extents = Extents(local_datetime(2014, 3, 28, 11, 11), 'month')
        # self.assert_extents(extents, (2014, 3, 1, 0, 0, 0), (2014, 3, 31, 23, 59, 59))

    def test_extents_year(self):
        extents = Extents(local_datetime(2014, 2, 18, 11, 11, 11), 'year')

        self.assert_extents(extents, (2014, 1, 1, 0, 0, 0), (2014, 12, 31, 23, 59, 59))
        # this fails if I start with a date in DST

    def test_period_set_invalid(self):
        extents = Extents(local_datetime(2014, 6, 18))

        self.assertRaises(ValueError, lambda: extents.set_period('lightyear'))

    def test_period_undefinde(self):
        extents = Extents(local_datetime(2014, 6, 18))

        self.assertRaises(ValueError, lambda: list(extents))

    def test_period_defined(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), period='day')

        self.assert_extents(extents, (2014, 6, 18, 0, 0, 0), (2014, 6, 18, 23, 59, 59))

        # period can be changed
        extents.set_period('month')
        self.assert_extents(extents, (2014, 6, 1), (2014, 6, 30, 23, 59, 59))

    def test_period_previous(self):
        t = datetime(2014, 6, 18, 11, 11, 11, tzinfo=utc)
        extents = Extents(t, period='week')

        self.assertEqual(extents.previous(), local_datetime(2014, 6, 12))

    def test_period_next(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), period='week')

        self.assertEqual(extents.next(), local_datetime(2014, 6, 26,))

        extents = Extents(local_datetime(2014, 6, 25, 11, 11), period='week')
        self.assertEqual(extents.next(), local_datetime(2014, 7, 3))

        extents = Extents(local_datetime(2015, 4, 14, 11, 11), period='week')
        self.assertEqual(extents.next(), local_datetime(2015, 4, 23))

    def test_extents_to_string(self):
        t = local_datetime(2014, 6, 18, 11, 11, 11)
        t_formatted = t.__repr__()

        extents = Extents(t)
        self.assertEqual(str(extents), 'Extents for undefined period around %s' % t_formatted)

        extents.set_period('week')
        self.assertEqual(str(extents), 'Extents for `week` around %s' % t_formatted)

    def test_slices_in_day(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), 'day')

        self.assertEqual(extents.slices('hour'), 24)
        self.assertEqual(extents.slices('15minute'), 24 * 4)

    def test_slices_in_week(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), 'week')

        self.assertEqual(extents.slices('day'), 7)
        self.assertEqual(extents.slices('hour'), 7 * 24)
        self.assertEqual(extents.slices('15minute'), 7 * 24 * 4)

    def test_slices_illigal_interval(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11), 'week')

        self.assertRaises(ValueError, lambda: extents.slices('year'))

    def test_for_period(self):
        extents = Extents(local_datetime(2014, 6, 18, 11, 11, 11))

        start, end = extents.for_period('week')
        self.assertEqual(start, local_datetime(2014, 6, 16, 0, 0, 0))
        self.assertEqual(end, local_datetime(2014, 6, 22, 23, 59, 59))
