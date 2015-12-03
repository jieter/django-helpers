from django.test import SimpleTestCase, TestCase

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator
from django.template import Context, Template
from django.test.utils import override_settings


class TestAnalyticsTag(SimpleTestCase):
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


class TestPaginatorTag(TestCase):
    template = Template('{% load paginator %}{% paginator items %}')

    def test_paginator(self):
        # create some users
        for i in range(20):
            User.objects.create(
                email='test%d@example.com' % i,
                username='test%d' % i
            )

        paginator = Paginator(User.objects.all(), 10)

        rendered = self.template.render(Context({
            'items': paginator.page(1)
        }))
        self.assertTrue('Page 1 of 2' in rendered)

        rendered = self.template.render(Context({
            'items': paginator.page(2)
        }))
        self.assertTrue('Page 2 of 2' in rendered)

    def test_paginator_single_page(self):
        paginator = Paginator(User.objects.all(), 10)

        rendered = self.template.render(Context({
            'items': paginator.page(1)
        }))
        self.assertEquals(rendered, '')
