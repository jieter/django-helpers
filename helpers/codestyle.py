from django.conf import settings
from django.test import SimpleTestCase
from flake8.engine import get_style_guide


class CodingStyle(SimpleTestCase):
    flake8 = get_style_guide(
        ignore=('E501', 'F401', 'F403', 'E128', 'F999'),
        report=None,
        exclude=['*/migrations/*']
    )

    def test_flake8(self):
        report = self.flake8.check_files([settings.BASE_DIR])

        self.assertEqual(report.get_statistics('E'), [], 'Flake8 reports errors')
