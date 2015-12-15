import random
import bisect

from .. import UNSET
from .._value import Value
from ._field import Field


class FormattedString(Field):
    @staticmethod
    def init(self, context_key):
        super(self.__class__, self).__init__()

        self._context_key = context_key

        for param, choices in self.format_parameters.iteritems():
            for choice in choices:
                attr = '{0}_{1}'.format(param, choice)
                setattr(self, attr, Value(context_key))

    @staticmethod
    def get_value_data(self, context):
        result = {}
        for param, choices in self.format_parameters.iteritems():
            result[param] = {}
            for choice in choices:
                attr = '{0}_{1}'.format(param, choice)
                attr = getattr(self, attr)
                result[param][choice] = attr[context]
        return result

    @staticmethod
    def put_value_data(self, context, **value_data):
        for param in self.format_parameters:
            try:
                values_weights = value_data[param]
            except KeyError:
                continue
            for value, weight in values_weights.iteritems():
                attr = '{0}_{1}'.format(param, value)
                attr = getattr(self, attr)
                attr[context] = weight

    @staticmethod
    def compute(self, context):
        result = {}
        for param, param_values in self.format_parameters.iteritems():
            choices = []
            for param_value in param_values:
                attr = '{0}_{1}'.format(param, param_value)
                weight = getattr(self, attr)[context]
                if weight is UNSET:
                    break
                choices.append((param_value, weight))
            if choices:
                result[param] = FormattedString._select_param_value(choices)
        if not result:
            return UNSET
        result = self.format_string.format(**result)
        return result

    @staticmethod
    def _select_param_value(choices):
        """
        Source: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        Author: Raymond Hettinger
        """
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random.random() * total
        i = bisect.bisect(cum_weights, x)
        return values[i]
