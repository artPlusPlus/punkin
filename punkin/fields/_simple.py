from .._util import UNSET
from .._value import Value
from ._field import Field


class Simple(Field):
    @staticmethod
    def init(self, context_key):
        super(self.__class__, self).__init__()

        self._context_key = context_key
        self.value = Value(context_key)

    @staticmethod
    def put_value_data(self, context, **value_data):
        self.value[context] = value_data.get('value', UNSET)

    @staticmethod
    def compute(self, context):
        return self.value[context]
