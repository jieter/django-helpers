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
        self.assertIn('test_exception.py', message)

        # should contain the message:
        self.assertIn(the_message, message)

        # should contain the line raising the Exception
        self.assertIn('raise TestException(the_message)', message)
