from django.test import SimpleTestCase

from helpers.util import Wrapper


class Klass(object):

    def __init__(self, bar):
        self.bar = bar

    def get_bar(self):
        return self.bar


class Wrapped(Wrapper):
    pass


TEST_OBJ = {'a': 2, 'b': 3}


class TestWrapper(SimpleTestCase):
    def test_wrapper_get(self):
        wrapped = Wrapped(Klass(TEST_OBJ))

        self.assertEquals(wrapped.get_bar(), TEST_OBJ)

    def test_wrapper_set(self):
        wrapped = Wrapped(Klass({}))

        self.assertNotEquals(wrapped.get_bar(), TEST_OBJ)
        self.assertEquals(wrapped.get_bar(), {})

        wrapped.bar = TEST_OBJ

        self.assertEquals(wrapped.get_bar(), TEST_OBJ)
