class Table(object):
    def __init__(self, context_key=None):
        self._context_key = context_key
        self._rows = None

    def add_row(self, context, field_name, **value_data):
        field = getattr(self, field_name)
        field.put_value_data(context, **value_data)

    def import_json(self, json_data):
        self._context_key = json_data['context_key']

        row_data = json_data['rows']
        for row in row_data:
            context = {self._context_key: row['context_value']}
            field_data = row['field_data']
            for field in field_data:
                field_name = field['name']
                value_data = field['value_data']

                self.add_row(context, field_name, **value_data)
