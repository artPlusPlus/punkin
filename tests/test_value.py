from punkin import UNSET
from punkin._value import Value


def test_value_initialization():
    value = Value('test')

    assert isinstance(value, Value)

    value = Value('test', setter=lambda x: x)
    assert value._setter != None
    assert isinstance(value, Value)


def test_value_set_without_setter():
    context = {'test': 'success'}
    value = Value('test')

    value[context] = 'bar'

    assert value[context] == 'bar'


def test_value_set_with_setter():
    context = {'test': 'success'}
    value = Value('test', setter=lambda x: x)

    value[context] = 'baz'

    assert value[context] == 'baz'


def test_value_get_without_setter():
    context = {'test': 'success'}
    value = Value('test')

    value[context] = 'bax'

    assert value[context] == 'bax'


def test_value_get_with_setter():
    context = {'test': 'success'}
    value = Value('test', setter=lambda x: 'bav')

    value[context] = 'baf'

    assert value[context] == 'bav'


def test_value_get_unset():
    context = {'test': 'success'}
    value = Value('test')

    assert value[context] is UNSET


def test_value_merge_target_unset():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}

    default = Value('default')
    default[context] = 'Foo'

    override = Value('override')

    merged = Value('merged')

    merged.merge(default, context)
    assert merged[context] == 'Foo'

    merged.merge(override, context)
    assert merged[context] == 'Foo'


def test_value_merge_source_unset():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}

    default = Value('default')
    override = Value('override')
    override[context] = 'baw'

    merged = Value('merged')

    merged.merge(default, context)
    assert merged[context] is UNSET

    merged.merge(override, context)
    assert merged[context] == 'baw'


def test_value_merge():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}

    default = Value('default')
    default[context] = 'foo'

    override = Value('override')
    override[context] = 'bar'

    merged = Value('merged')

    merged.merge(default, context)
    assert merged[context] == 'foo'

    merged.merge(override, context)
    assert merged[context] == 'bar'
