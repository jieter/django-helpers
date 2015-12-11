from django.test import SimpleTestCase
from helpers.exception import exception_message


class TestException(Exception):
    pass


class ExceptionTest(SimpleTestCase):

    def test_backtrace(self):
        the_message = 'Something went horribly wrong'
        try:
            raise TestException(the_message)
        except TestException:
            message = exception_message()

        # should contain current file:
        self.assertTrue('test_exception.py' in message)

        # should contain the message:
        self.assertTrue(the_message in message)

        # should contain the line raising the Exception
        self.assertTrue('raise TestException(the_message)' in message)
