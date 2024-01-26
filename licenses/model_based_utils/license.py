import datetime
import json

# noinspection PyUnreachableCode
if False:
    from licenses.models import License  # fake import for type hint


def as_dict(entry, serializable=False):
    related_fields = [field for field in entry.meta.get_fields() if 'Rel' in f'{type(field)}']
    entry: License
    data = {}
    for key, value in entry.__dict__.items():
        if not key.startswith('_'):
            if serializable:
                if isinstance(value, datetime.date):
                    value = f'{value}'
                if isinstance(value, datetime.datetime):
                    value = f'{value}'
            data[key] = value
            if key.endswith('_id'):
                new_key = key.replace('_id', '')
                data[new_key] = f'{getattr(entry, new_key)}'
    for related_field in related_fields:
        data[related_field.name] = []
        for related_entry in getattr(entry, f'{related_field.name}').all():
            if hasattr(related_entry, 'as_dict'):
                if serializable:
                    related_entry_as_dict = related_entry.as_dict(serializable=True)
                else:
                    related_entry_as_dict = related_entry.as_dict
            else:
                related_entry_as_dict = {}
                for key, value in related_entry.__dict__.items():
                    if not key.startswith('_'):
                        if serializable:
                            if isinstance(value, datetime.date):
                                value = f'{value}'
                            if isinstance(value, datetime.datetime):
                                value = f'{value}'
                        related_entry_as_dict[key] = value

            data[related_field.name].append(related_entry_as_dict)

    return data
