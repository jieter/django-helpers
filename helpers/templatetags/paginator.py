from django import template
from django.utils.html import format_html
from django.utils.translation import ugettext as _

register = template.Library()

link_fmt = '<a href="?page={}" class="btn btn-primary">{}</a>'


@register.simple_tag
def paginator(items):
    if not items.paginator.num_pages > 1:
        return ''

    if items.has_previous():
        prev_link = format_html(link_fmt, items.previous_page_number, _('Vorige'))
    else:
        prev_link = ''

    pages = 'Page {} of {}'.format(items.number, items.paginator.num_pages)

    if items.has_next():
        next_link = format_html(link_fmt, items.next_page_number, _('Volgende'))
    else:
        next_link = ''

    return format_html(
        '''<div class="row">
            <div class="col-sm-4">{}</div>
            <div class="col-sm-4 text-center">{}</div>
            <div class="col-sm-4 text-right">{}</div>
        </div>''',
        prev_link,
        pages,
        next_link
    )
