from django.conf import settings


def googleanalytics(request):  # pragma: nocover
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', None),
    }
