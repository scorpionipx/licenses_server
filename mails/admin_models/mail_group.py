from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
)

from django.utils.html import format_html

from mails.models import MailAddress


class MailAddressInline(TabularInline):
    """MailAddressInline

    """
    model = MailAddress
    extra = 0


class MailGroupAdmin(ModelAdmin):
    """MailGroupAdmin

    """
    fields = (
        # all
    )
    exclude = (
        'mails',
    )
    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'description',
        'plain_receivers',
        'author',
        'pk',
        'created',
    )

    list_filter = (
        # none
    )

    ordering = (
        'name',
    )

    inlines = [
        MailAddressInline,
    ]

    empty_value_display = '-empty-'
    list_per_page = 20

    filter_horizontal = (
        'mails',
        'users',
    )

    @staticmethod
    def plain_receivers(instance):
        """plain_receivers

        """
        html = f'<a href="{instance.receivers_plain_url}" target="_blank">link</a>'
        return format_html(html)

    def get_form(self, request, obj=None, **kwargs):
        """get_form

            Custom form with altered users field.
        """
        form = super(MailGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['users'].label_from_instance = lambda user: '{} {} - {}'.format(
            user.first_name,
            user.last_name,
            user.username,
        )

        form.base_fields['author'].label_from_instance = lambda user: '{} {} - {}'.format(
            user.first_name,
            user.last_name,
            user.username,
        )
        return form
