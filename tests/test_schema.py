from punkin._schema import Schema
from punkin.fields import *


_schema_data = {
    'name': 'ffx_schema',
    'field_data': [
        {
            'field_name': 'name',
            'field_type': 'Simple',
            'static_parameters': {}
        },
        {
            'field_name': 'size',
            'field_type': 'FloatRange',
            'static_parameters': {}
        },
        {
            'field_name': 'target',
            'field_type': 'FormattedString',
            'static_parameters': {
                'format': '{color}_{series}',
                'format_parameters': {
                    'color': [
                        'RED',
                        'BLUE',
                        'GREEN'
                    ],
                    'series': [
                        '00'
                    ]
                }
            }
        }
    ]
}


def test_schema_instantiation():
    schema = Schema('success')

    assert isinstance(schema, Schema)


def test_schema_import_json():
    schema = Schema.import_from_json(_schema_data)

    assert isinstance(schema.name, Simple)
    assert isinstance(schema.size, FloatRange)
    assert isinstance(schema.target, FormattedString)


def test_schema_create_table():
    schema = Schema.import_from_json(_schema_data)
    table = schema.create_table('default')

    assert isinstance(table.name, schema.name)
    assert isinstance(table.size, schema.size)
    assert isinstance(table.target, schema.target)
