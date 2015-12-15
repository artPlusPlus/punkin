from punkin import UNSET
from punkin.fields import FormattedString


_FORMAT_STRING = '{color}_{series}'
_FORMAT_PARAMS = {'color': ['RED', 'BLUE', 'GREEN'],
                  'series': ['00']}


def test_formatted_string_instantiation():
    field_cls = FormattedString('Color',
                                format_string=_FORMAT_STRING,
                                format_parameters=_FORMAT_PARAMS)

    assert isinstance(field_cls, FormattedString)
    assert field_cls.format_string == _FORMAT_STRING
    assert field_cls.format_parameters == _FORMAT_PARAMS

    field_inst = field_cls('default')

    assert isinstance(field_inst, field_cls)
    assert field_inst._context_key == 'default'


def test_formatted_string_unset():
    field_cls = FormattedString('Color',
                                format_string=_FORMAT_STRING,
                                format_parameters=_FORMAT_PARAMS)
    field_inst = field_cls('default')

    context = {'default': 'default'}
    assert field_inst.compute(context) is UNSET


def test_formatted_string_set():
    context = {'default': 'default'}
    field_cls = FormattedString('Color',
                                format_string=_FORMAT_STRING,
                                format_parameters=_FORMAT_PARAMS)

    field_inst = field_cls('default')
    field_inst.color_RED[context] = 1
    field_inst.color_BLUE[context] = 0
    field_inst.color_GREEN[context] = 0
    field_inst.series_00[context] = 1

    result = field_inst.compute(context)

    assert result == 'RED_00'


def test_formatted_string_merge():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}
    field_cls = FormattedString('Color',
                                format_string=_FORMAT_STRING,
                                format_parameters=_FORMAT_PARAMS)

    default = field_cls('default')
    default.color_RED[context] = 1
    default.color_BLUE[context] = 0
    default.color_GREEN[context] = 0
    default.series_00[context] = 1

    override = field_cls('override')
    override.color_RED[context] = 0
    override.color_BLUE[context] = 1
    override.color_GREEN[context] = 0

    merged = field_cls('merged')
    merged.merge(default, context)
    merged.merge(override, context)

    assert merged.color_RED[context] == 0
    assert merged.color_BLUE[context] == 1
    assert merged.color_GREEN[context] == 0
    assert merged.series_00[context] == 1
