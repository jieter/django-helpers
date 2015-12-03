from django.conf import settings
from django.db import connection
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def tag(name, contents):
    return format_html('<{}>{}</{}>', name, mark_safe(contents), name)


def tr(contents):
    return tag('tr', contents)


def th(contents):
    return tag('th', contents)


def td(contents):
    return tag('td', contents)


class Statistic(object):
    def __init__(self, name, keys=None, description=None):
        self.name = name
        self.stats = []

        self.description = description
        self.keys = keys

    def slug(self):
        return self.name.replace(' ', '-')

    @classmethod
    def from_queryset(self, name, queryset, *args, **kwargs):
        return self.from_iterable(name, queryset, *args, **kwargs)

    @classmethod
    def from_iterable(self, name, datasource, *args, **kwargs):
        stats = Statistic(name, *args, **kwargs)

        if isinstance(datasource, QuerySet):
            datasource = datasource.values_list()

        for r in list(datasource):
            stats.add(r)
        return stats

    def add(self, *args):
        self.stats.append(*args)

    def render_rows(self):
        html = ''

        # header, if defined.
        if (self.keys is not None):
            html += tr(''.join(map(th, self.keys))) + '\n'

        for row in self.stats:
            html += tr(''.join(map(td, row))) + '\n'

        return mark_safe(html)


def postgres_table_size_stats():  # pragma: no cover
    if not settings.DATABASES['default']['ENGINE'].endswith('postgresql_psycopg2'):
        return Statistic('DB statistics only available on PostgreSQL')

    query = '''SELECT
        table_name,
        pg_size_pretty(table_size) AS table_size,
        pg_size_pretty(indexes_size) AS indexes_size,
        pg_size_pretty(total_size) AS total_size
    FROM (
        SELECT
            table_name,
            pg_table_size(table_name) AS table_size,
            pg_indexes_size(table_name) AS indexes_size,
            pg_total_relation_size(table_name) AS total_size
        FROM (
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        ) AS all_tables
        ORDER BY total_size DESC
    ) AS pretty_sizes'''

    cursor = connection.cursor()
    cursor.execute(query)

    return Statistic.from_iterable('PostgreSQL table size',
        cursor,
        keys=('table', 'data', 'indexes', 'total')
    )
