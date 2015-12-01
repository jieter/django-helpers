from django.conf import settings


def googleanalytics(request):  # pragma: nocover
    'Deprecated, use the templatetag in helpers.templatetags.analytics'
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', None),
    }
