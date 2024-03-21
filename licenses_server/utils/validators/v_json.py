import json

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


def validate_json(value):
    try:
        json.loads(value)
    except Exception as exception:
        assert exception
        raise ValidationError(
            _("%(value)s is not a valid JSON format"),
            params={"value": value},
        )
