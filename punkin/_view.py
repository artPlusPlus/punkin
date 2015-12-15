from .fields._field import Field


class View(object):
    def __init__(self):
        self._tables = []

    def _iter_fields(self):
        for name, attr in self.__dict__.iteritems():
            if isinstance(attr, Field):
                yield name, attr

    def add_table(self, table):
        self._tables.append(table)

    def compute(self, **context):
        context['__view__'] = '__view__'
        result = {}
        for field_name, view_field in self._iter_fields():
            view_field = view_field('__view__')
            for table in self._tables:
                table_field = getattr(table, field_name)
                view_field.merge(table_field, context)
            result[field_name] = view_field.compute(context)
        return result
