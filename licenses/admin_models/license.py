from django.contrib import admin


from licenses.models import Constraint


class ConstraintInline(admin.TabularInline):
    model = Constraint


class LicenseAdmin(admin.ModelAdmin):
    """LicenseAdmin

    """
    fields = (
        # all
    )
    exclude = (
        # nothing
    )
    search_fields = (
        # none
    )

    list_display = (
        'application',
        'archived',
        'expiry_date',
        'author',
        'pk',
        'created',
    )
    list_filter = (
        'application',
        'archived',
    )
    ordering = (
        '-created',
    )
    empty_value_display = '-empty-'
    list_per_page = 20

    inlines = [
        ConstraintInline,
    ]

    def has_change_permission(self, request, obj=None):
        return False
