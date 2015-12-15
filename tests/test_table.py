from punkin._table import Table
from punkin.fields import Simple
from punkin.fields import FloatRange
from punkin.fields import FormattedString


_table_json = {
    'context_key': 'default',
    'rows': [
        {
            'context_value': 'default',
            'field_data': [
                {
                    'name': 'name',
                    'value_data': {
                        'value': 'Success'
                    }
                },
                {
                    'name': 'magnitude',
                    'value_data': {
                        'minimum': 6.0,
                        'maximum': 7.0,
                        'precision': 0.01,
                        'sign_start': 1,
                        'sign_end': 1
                    }
                },
                {
                    'name': 'target',
                    'value_data': {
                        'color': {
                            'RED': 1,
                            'GREEN': 0,
                            'BLUE': 0
                        },
                        'series': {
                            '00': 1
                        }
                    }
                }
            ]
        }
    ]
}


def test_table_instantiation():
    table = Table()
    table.name = Simple('name')('default')
    table.magnitude = FloatRange('magnitude')('default')
    table.target = FormattedString(
            'target',
            format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']}
    )('default')

    assert isinstance(table, Table)


def test_table_field_set():
    context = {'default': 'default'}

    table = Table('default')
    table.name = Simple('name')('default')
    table.magnitude = FloatRange('magnitude')('default')
    table.target = FormattedString(
            'target', format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']})('default')

    table.name.put_value_data(context,
                              value='Foo')
    table.magnitude.put_value_data(context,
                                   minimum=0.3,
                                   maximum=0.4,
                                   precision=0.01,
                                   sign_start=-1,
                                   sign_end=-1)
    table.target.put_value_data(context,
                                color={'RED': 0, 'BLUE': 4, 'GREEN': 2},
                                series={'00': 1})

    assert table.name.compute(context) == 'Foo'
    assert -0.4 <= table.magnitude.compute(context) <= -0.3
    assert table.target.compute(context) in ['BLUE_00', 'GREEN_00']


def test_table_import_json():
    context = {'default': 'default'}

    table = Table('default')
    table.name = Simple('name')('default')
    table.magnitude = FloatRange('magnitude')('default')
    table.target = FormattedString(
            'target', format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']})('default')

    table.import_json(_table_json)

    assert table.name.compute(context) == 'Success'
    assert 6.0 <= table.magnitude.compute(context) <= 7.0
    assert table.target.compute(context) == 'RED_00'
