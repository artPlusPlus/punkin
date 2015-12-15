import collections

from .._util import UNSET
from .._value import Value


class Field(type):
    _field_types = {}

    def __new__(mcs, name, **static_parameters):
        bases = tuple([object])

        attrs = static_parameters.copy()
        attrs['__module__'] = __name__
        attrs['__metaclass__'] = mcs
        attrs['__init__'] = mcs.init
        attrs['_iter_values'] = mcs._iter_values
        attrs['put_value_data'] = mcs.put_value_data
        attrs['get_value_data'] = mcs.get_value_data
        attrs['compute'] = mcs.compute
        attrs['merge'] = mcs.merge

        result = super(Field, mcs).__new__(mcs, name, bases, attrs)

        return result

    def __init__(cls, *args, **kwargs):
        super(Field, cls).__init__(*args)

    @staticmethod
    def init(self, context_key):
        raise NotImplementedError()

    @staticmethod
    def get_value_data(self, context):
        result = {}
        for name, value in self._iter_values():
            result[name] = value[context]
        return result

    @staticmethod
    def put_value_data(self, context, **value_data):
        for name, value in self._iter_values():
            value[context] = value_data.get(name, UNSET)

    @staticmethod
    def compute(self, context):
        raise NotImplementedError()

    @staticmethod
    def merge(self, source, context):
        result = {}
        for tgt_name, tgt_value in self._iter_values():
            src_value = getattr(source, tgt_name)
            if not isinstance(src_value, Value):
                # TODO: Raise error
                continue
            tgt_value.merge(src_value, context)
        return result

    @classmethod
    def get_field_type(mcs, type_name):
        queue = collections.deque([mcs])
        while queue:
            cls = queue.popleft()
            if cls.__name__ == type_name:
                return cls
            for cls in cls.__subclasses__(cls):
                queue.append(cls)
        return None

    @staticmethod
    def _iter_values(self):
        for name, attr in self.__dict__.iteritems():
            if isinstance(attr, Value):
                yield name, attr

get_field_type = Field.get_field_type
