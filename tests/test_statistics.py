from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from helpers.statistics import Statistic


class TestStatistic(SimpleTestCase):
    def test_statistic(self):
        stat = Statistic('Test', keys=['foo', 'bar'], description='Statistic Example')
        stat.add([1, 2])

        self.assertEqual(stat.slug(), 'Test')

        table = stat.render_rows()

        self.assertEqual(table, '<tr><th>foo</th><th>bar</th></tr>\n<tr><td>1</td><td>2</td></tr>\n')

    def test_statistic_from_iterable(self):
        datasource = zip(range(10), range(10, 20))
        stat = Statistic.from_iterable(
            'Test iterable', datasource,
            keys=['foo', 'bar']
        )


class TestStatisticQueryset(TestCase):
    def test_statistic_from_queryset(self):
        User.objects.create(email='test@example.com', username='test')
        User.objects.create(email='test2@example.com', username='test2')

        stat = Statistic.from_queryset('Number of users', User.objects.all())

        table = stat.render_rows()
