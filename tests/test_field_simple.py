from punkin import UNSET
from punkin.fields import Simple


def test_simple_instantiation():
    field_cls = Simple('name')

    assert isinstance(field_cls, Simple)

    field_inst = field_cls('default')

    assert isinstance(field_inst, field_cls)
    assert field_inst._context_key == 'default'


def test_simple_unset():
    context = {'default': 'default'}

    field_cls = Simple('name')
    field_inst = field_cls('default')

    assert field_inst.compute(context) is UNSET


def test_simple_set():
    context = {'default': 'default'}

    field_cls = Simple('name')
    field_inst = field_cls('default')
    field_inst.value[context] = 'success'

    assert field_inst.compute(context) == 'success'


def test_simple_merge():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}

    field_cls = Simple('name')

    default = field_cls('default')
    default.value[context] = 'foo'

    override = field_cls('override')
    override.value[context] = 'bar'

    merged = field_cls('merged')

    merged.merge(default, context)
    assert merged.value[context] == 'foo'

    merged.merge(override, context)
    assert merged.value[context] == 'bar'
