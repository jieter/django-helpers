from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()

script_fmt = '''<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', '{}', '{}');
ga('send', 'pageview');
</script>'''


@register.simple_tag
def googleanalytics():  # pragma: nocover
    if not hasattr(settings, 'GOOGLE_ANALYTICS'):
        return ''

    return format_html(script_fmt, *settings.GOOGLE_ANALYTICS)
