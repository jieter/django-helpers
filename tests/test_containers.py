from django.test import SimpleTestCase
from helpers.containers import TimeseriesContainer
from helpers.time import local_datetime


class TimeseriesContainerTest(SimpleTestCase):

    def test_simple(self):
        keys = ('foo', 'bar')

        values = (
            (1, 2.4440404),
            (2, 4.4)
        )

        d = TimeseriesContainer(keys, values)

        self.assertEquals(d[0], dict(foo=1, bar=2.4440404))
        self.assertEquals(d[1], dict(foo=2, bar=4.4))

        d.prepare_for_view()

        self.assertEquals(d[0], dict(foo=1, bar=2.44))
        self.assertEquals(d[1], dict(foo=2, bar=4.4))

    def test_invalid(self):
        '''not the right number of keys.'''
        keys = ('foo', )
        values = (
            (1, 2, 3),
            (3, 4, 5)
        )

        self.assertRaises(ValueError, lambda: TimeseriesContainer(keys, values))

    def test_empty(self):
        keys = ['foo', 'bar']

        d = TimeseriesContainer(keys, [])

        self.assertEquals(len(d), 0)
        self.assertItemsEqual(d.keys, keys)

    def test_indexError(self):
        d = TimeseriesContainer(['foo'], [])
        self.assertRaises(IndexError, lambda: d[1])

    def test_iter(self):
        keys = ('foo', 'bar', 'baz')
        values = (
            (1, 2, 4),
            (2, 4, 8),
            (3, 6, 12),
            (4, 8, 16)
        )
        self.assertEquals(len(values), 4)

        for i, it in enumerate(TimeseriesContainer(keys, values)):
            self.assertTrue(isinstance(it, dict))
            self.assertItemsEqual(it.keys(), keys)

    def test_sum(self):
        keys = ('foo',)
        values = (
            (1, ),
            (2, ),
            (3, ),
            (4, )
        )
        container = TimeseriesContainer(keys, values)

        self.assertEqual(container.sum('foo'), 10)

    def test_to_json(self):
        keys = ['timestamp', 'foo']
        values = (
            (local_datetime(2015, 1, 1, 12, 0, 0), 1),
            (local_datetime(2015, 1, 2, 12, 0, 0), 2),
            (local_datetime(2015, 1, 3, 12, 0, 0), 3),
            (local_datetime(2015, 1, 4, 12, 0, 0), 4)
        )
        container = TimeseriesContainer(keys, values)

        data = container.to_json_dict(extra='foo')

        self.assertEquals(data['keys'], keys)
        self.assertEquals(data['extra'], 'foo')
