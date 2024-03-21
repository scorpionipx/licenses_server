from django.contrib import admin

from django.utils.html import format_html


from licenses.models import License
from licenses.model_based_utils.license import generate_serial_no


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
        'as_json_urls',
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

    @staticmethod
    def as_json_urls(entry):
        """as_json_urls

            Custom field display for admin view.
        :param entry: target entry
        """
        html = f'<a href="{entry.as_json_url}">link</a> / <a href="{entry.as_json_for_humans_url}">link 4 humans</a>'
        return format_html(html)
    as_json_urls.short_description = 'As JSON'

    def get_changeform_initial_data(self, request):
        initial_data = {'serial_no': generate_serial_no(request, License), 'author': request.user}
        print(initial_data)
        return initial_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # On update type_name will be read-only
            readonly_fields = (
                'author',
                'serial_no',
                'created',
            )
            return readonly_fields
        else:
            # On creation all fields will be editable
            readonly_fields = (
                'created',
            )
            return readonly_fields
