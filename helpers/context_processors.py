from django.conf import settings


def googleanalytics(request):
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', None),
    }
