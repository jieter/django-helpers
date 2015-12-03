from django.test import SimpleTestCase

from django.template import Context, Template
from django.test.utils import override_settings


class TestTemplatetags(SimpleTestCase):

    def test_analytics_without_setting(self):
        template = Template('{% load analytics %}{% googleanalytics %}')

        rendered = template.render(Context({}))

        self.assertEqual(rendered, '')

    @override_settings(GOOGLE_ANALYTICS=('UA-foo', 'jieter.nl'))
    def test_analytics(self):
        template = Template('{% load analytics %}{% googleanalytics %}')

        rendered = template.render(Context({}))

        self.assertTrue(rendered.startswith('<script>'))
        self.assertTrue(rendered.endswith('</script>'))
        self.assertTrue("ga('create', 'UA-foo', 'jieter.nl')" in rendered)
