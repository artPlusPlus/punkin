import random
import decimal

from .. import UNSET
from .._value import Value
from ._field import Field


_MIN_MAX_SETTER = lambda v: abs(float(v))
_SIGN_SETTER = lambda v: v/abs(v)


class FloatRange(Field):
    @staticmethod
    def init(self, context_key):
        super(self.__class__, self).__init__()
        self._context_key = context_key

        self.minimum = Value(context_key, setter=_MIN_MAX_SETTER)
        self.maximum = Value(context_key, setter=_MIN_MAX_SETTER)
        self.precision = Value(context_key)
        self.sign_start = Value(context_key, setter=_SIGN_SETTER)
        self.sign_end = Value(context_key, setter=_SIGN_SETTER)

    @staticmethod
    def compute(self, context):
        min = self.minimum[context]
        max = self.maximum[context]
        prec = self.precision[context]
        sign_start = self.sign_start[context]
        sign_end = self.sign_end[context]

        if UNSET in (min, max, prec, sign_start, sign_end):
            return UNSET

        sign = random.choice((sign_start, sign_end))
        result = random.uniform(min, max)
        result *= sign

        with decimal.localcontext() as ctx:
            ctx.prec = prec
            result = float(decimal.Decimal(result))

        return result
