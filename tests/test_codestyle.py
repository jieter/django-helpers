from django.test import SimpleTestCase
from flake8.engine import get_style_guide

flake8 = get_style_guide(
    ignore=('E501', 'F403', 'E128'),
    report=None,
    exclude=['*/migrations/*']
)


class CodingStyle(SimpleTestCase):
    def test_flake8(self):
        report = flake8.check_files(['helpers/'])

        self.assertEqual(report.get_statistics('E'), [], 'Flake8 reports errors')
