from django.contrib import admin


from licenses.admin_models.application import *
from licenses.admin_models.license import LicenseAdmin


from licenses.models import (
    Application,
    Constraint,
    Event,
    License,
)


admin.site.register(Application)
admin.site.register(Constraint)
admin.site.register(Event)
admin.site.register(License, LicenseAdmin)
