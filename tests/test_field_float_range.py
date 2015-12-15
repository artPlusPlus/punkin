from punkin import UNSET
from punkin.fields import FloatRange


def test_float_range_instantiation():
    field_cls = FloatRange('magnitude')

    assert isinstance(field_cls, FloatRange)

    field_inst = field_cls('default')

    assert isinstance(field_inst, field_cls)
    assert field_inst._context_key == 'default'


def test_float_range_unset():
    context = {'default': 'default'}
    field_cls = FloatRange('magnitude')
    field_inst = field_cls('default')

    assert field_inst.compute(context) is UNSET


def test_float_range_set():
    context = {'default': 'default'}

    field_cls = FloatRange('magnitude')

    field_inst = field_cls('default')
    field_inst.minimum[context] = 0.3
    field_inst.maximum[context] = 0.4
    field_inst.precision[context] = 0.01
    field_inst.sign_start[context] = -1
    field_inst.sign_end[context] = -1

    result = field_inst.compute(context)

    assert -0.4 < result < -0.3


def test_float_range_merge():
    context = {'default': 'default',
               'override': 'not_default',
               'merged': 'merged'}
    field_cls = FloatRange('magnitude')

    default = field_cls('default')
    default.minimum[context] = 0.3
    default.maximum[context] = 0.4
    default.precision[context] = 0.01
    default.sign_start[context] = -1
    default.sign_end[context] = -1

    override = field_cls('override')
    override.maximum[context] = 0.8
    override.sign_start[context] = 1
    override.sign_end[context] = 1

    merged = field_cls('merged')
    merged.merge(default, context)
    merged.merge(override, context)

    assert merged.minimum[context] == 0.3
    assert merged.maximum[context] == 0.8
    assert merged.precision[context] == 0.01
    assert merged.sign_start[context] == 1
    assert merged.sign_end[context] == 1
