from .fields import get_field_type
from .fields._field import Field
from ._table import Table
from ._view import View


class Schema(object):
    @property
    def schema_name(self):
        return self._name

    @property
    def fields(self):
        if self._fields is None:
            self._fields = []
            for attr in self.__dict__.itervalues():
                if isinstance(attr, Field):
                    self._fields.append(attr)
        return self._fields

    def __init__(self, name):
        self._name = name
        self._fields = None

    @classmethod
    def import_from_json(cls, schema_data):
        schema_name = schema_data['name']

        result = cls(schema_name)
        for field_data in schema_data['field_data']:
            field_name = field_data['field_name']
            field_type_name = field_data['field_type']
            field_static_params = field_data['static_parameters']
            field_type = get_field_type(field_type_name)
            field = field_type(field_name, **field_static_params)
            setattr(result, field_name, field)

        return result

    def create_table(self, context_key):
        result = Table(context_key)
        for field in self.fields:
            setattr(result, field.__name__, field(context_key))
        return result

    def create_view(self):
        result = View()
        for field in self.fields:
            setattr(result, field.__name__, field)

import_json_schema = Schema.import_from_json
