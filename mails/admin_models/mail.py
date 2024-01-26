from django.contrib.admin import ModelAdmin


class MailAdmin(ModelAdmin):
    """MailAdmin

    """
    fields = (
        # all
    )
    exclude = (
        # none
    )
    search_fields = (
        'test_item',
    )

    list_display = (
        'title',
        'app',
        'pk',
        'created',
    )

    list_filter = (
        'app',
    )

    ordering = (
        '-created',
    )

    empty_value_display = '-empty-'
    list_per_page = 20
