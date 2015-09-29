# from datetime import datetime, timedelta
#
# from django.test import SimpleTestCase, TestCase
# from django.utils.timezone import utc
#
# from coconut.apps.api.models import Flow, Meter
# from helpers.models import _group_by_multiple, group_by_interval
#
# # class GroupByIntervalTest(TestCase):
#     def setUp(self):
#
#         t = datetime(2015, 4, 16, 16, 1, 0, tzinfo=utc)
#         meter = Meter.objects.create(description='foo', mac='123')
#
#         def make(t, amount):
#             Flow.objects.create(timestamp=t, amount=amount, meter=meter)
#
#         make(t, 4)
#         make(t + timedelta(minutes=2), 10)
#         make(t + timedelta(minutes=2, seconds=10), 10)
#         make(t + timedelta(minutes=6), 20)
#         make(t + timedelta(minutes=20), 10)
#         make(t + timedelta(minutes=40), 10)
#
#     def group_by_interval(self, interval):
#         qs = Flow.objects.all()
#
#         return group_by_interval(qs, interval, (('amount', 'sum'), ))
#
#     def test_illegal_interval(self):
#         self.assertRaises(ValueError, lambda: self.group_by_interval('lightyear'))
#
#     def test_5hour(self):
#         values = self.group_by_interval('5hour')
#         self.assertEquals(len(values), 1)
#
#     def test_hour(self):
#         values = self.group_by_interval('hour')
#         self.assertEquals(len(values), 1)
#
#     def test_minute(self):
#         values = self.group_by_interval('minute')
#         self.assertEquals(len(values), 5)
#
#     def test_5minute(self):
#         values = self.group_by_interval('5minute')
#         self.assertEquals(len(values), 4)
#
#     # def test_key_order_is_preserved(self):
#     # TODO: implement test
#
#
# class GroupListByMinutesTest(SimpleTestCase):
#     def test_invalid(self):
#         self.assertRaises(AssertionError,
#             lambda: _group_by_multiple([[1, 2, 3]], 10, 'minute'))
#
#     def test_invalid_aggregate(self):
#         l = [
#             (datetime(2015, 1, 16, 16, 15, 12), 12),
#         ]
#         self.assertRaises(ValueError, lambda: _group_by_multiple(l, 5, 'minute', ('foo', )))
#
#     def test_empty(self):
#         self.assertEquals(_group_by_multiple([], 5, 'minute'), [])
#
#     def test_summing(self):
#         l = [
#             (datetime(2015, 1, 16, 16, 15, 12), 12),
#             (datetime(2015, 1, 16, 16, 15, 13), 12),
#             (datetime(2015, 1, 16, 16, 15, 14), 12),
#             (datetime(2015, 1, 16, 16, 16, 14), 12),
#
#             (datetime(2015, 1, 16, 16, 21, 14), 12),
#         ]
#
#         ret = _group_by_multiple(l, 5, 'minute')
#
#         self.assertEquals(ret, [
#             (datetime(2015, 1, 16, 16, 15, 0), 48),
#             (datetime(2015, 1, 16, 16, 20, 0), 12),
#         ])
#
#     def test_avg(self):
#         l = [
#             (datetime(2015, 1, 16, 16, 15, 12), 12),
#             (datetime(2015, 1, 16, 16, 15, 13), 1),
#             (datetime(2015, 1, 16, 16, 15, 14), 1),
#             (datetime(2015, 1, 16, 16, 16, 14), 1),
#
#             (datetime(2015, 1, 16, 16, 21, 14), 12),
#         ]
#
#         ret = _group_by_multiple(l, 5, 'minute', aggregates=('avg', ))
#         self.assertEquals(ret, [
#             (datetime(2015, 1, 16, 16, 15, 0), 3.75),
#             (datetime(2015, 1, 16, 16, 20, 0), 12.0),
#         ])
#
#     def test_combination(self):
#         l = [
#             (datetime(2015, 1, 16, 16, 15, 12), 12, 234, 1),
#             (datetime(2015, 1, 16, 16, 15, 13), 1, 200, 1),
#             (datetime(2015, 1, 16, 16, 15, 14), 1, 209, 1),
#             (datetime(2015, 1, 16, 16, 16, 14), 1, 0, 1),
#
#             (datetime(2015, 1, 16, 16, 21, 14), 12, 1, 2),
#         ]
#         ret = _group_by_multiple(l, 5, 'minute', aggregates=('avg', 'max', 'sum'))
#         self.assertEquals(ret, [
#             (datetime(2015, 1, 16, 16, 15, 0), 3.75, 234, 4),
#             (datetime(2015, 1, 16, 16, 20, 0), 12.0, 1, 2),
#         ])
