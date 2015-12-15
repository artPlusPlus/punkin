from . import UNSET


class Value(object):
    def __init__(self, context_key, setter=None):
        self._context_key = context_key
        self._setter = setter
        self._data = {}

    def __getitem__(self, context):
        try:
            return self._data[context[self._context_key]]
        except KeyError:
            return UNSET

    def __setitem__(self, context, value):
        if value is UNSET:
            try:
                del self[context]
            except KeyError:
                pass
            return
        if self._setter:
            value = self._setter(value)
        self._data[context[self._context_key]] = value

    def __delitem__(self, context):
        del self._data[context[self._context_key]]

    def merge(self, source_value, context):
        source_value = source_value[context]
        target_value = self[context]

        if source_value is UNSET:
            self[context] = target_value
        elif target_value is UNSET:
            self[context] = source_value
        else:
            # TODO: Handle merge operations (add, subtract, multiply, etc)
            # Example: self[context] = target_value * source_value
            self[context] = source_value
