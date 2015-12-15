import pytest

from punkin import View
from punkin._table import Table
from punkin.fields import Simple
from punkin.fields import FloatRange
from punkin.fields import FormattedString


def _create_context():
    context = {'default': 'default',
               'override': 'not_default'}
    return context


def _create_table(context_key):
    table = Table(context_key)
    table.name = Simple('name')(context_key)
    table.magnitude = FloatRange('magnitude')(context_key)
    table.target = FormattedString(
            'target', format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']})(context_key)

    return table


@pytest.fixture
def context():
    return _create_context()


@pytest.fixture
def default_table():
    _context = _create_context()
    result = _create_table('default')

    result.name.put_value_data(_context, value='Foo')
    result.magnitude.put_value_data(
            _context, minimum=0.3, maximum=0.4, precision=0.01, sign_start=-1,
            sign_end=-1)
    result.target.put_value_data(
            _context, color={'RED': 1, 'BLUE': 0, 'GREEN': 0}, series={'00': 1})

    return result

@pytest.fixture
def override_table():
    _context = _create_context()
    result = _create_table('override')

    result.name.put_value_data(_context, value='Bar')
    result.magnitude.put_value_data(
            _context, minimum=0.5, maximum=0.8)
    result.target.put_value_data(
            _context, color={'RED': 0, 'BLUE': 4, 'GREEN': 2}, series={'00': 1})

    return result


def test_view_instantiation():
    view = View()

    assert isinstance(view, View)


def test_view_add_table(default_table):
    view = View()
    view.add_table(default_table)

    assert default_table in view._tables


def test_view_default_compute(default_table, context):
    view = View()
    view.name = Simple('name')
    view.magnitude = FloatRange('magnitude')
    view.target = FormattedString(
            'target', format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']})

    view.add_table(default_table)

    result = view.compute(**context)

    assert result['name'] == 'Foo'
    assert -0.4 <= result['magnitude'] <= -0.3
    assert result['target'] == 'RED_00'


def test_view_merged_compute(default_table, override_table, context):
    view = View()
    view.name = Simple('name')
    view.magnitude = FloatRange('magnitude')
    view.target = FormattedString(
            'target', format_string='{color}_{series}',
            format_parameters={'color': ['RED', 'GREEN', 'BLUE'], 'series': ['00']})

    view.add_table(default_table)
    view.add_table(override_table)

    result = view.compute(**context)
    assert result['name'] == 'Bar'
    assert -0.8 <= result['magnitude'] <= -0.5
    assert result['target'] in ('BLUE_00', 'GREEN_00')
