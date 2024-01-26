from django.conf import settings

from django.http import HttpResponse

from django.views.generic import (
    View,
)


from mails.model_based_utils.mail import (
    DEVELOPMENT_RECEIVERS,
    DEVELOPMENT_TEMPLATES_DIR,

    join_paths,
    send_mail,
)


SERVER_URL = settings.URL_BASE


# STYLING_DEVELOPMENT_TEMPLATE = join_paths(DEVELOPMENT_TEMPLATES_DIR, 'styling.html')
STYLING_DEVELOPMENT_TEMPLATE = join_paths(DEVELOPMENT_TEMPLATES_DIR, '_layouts_', 'base_as_table.html')


class DevelopmentTestView(View):
    """DevelopmentTestView

    """

    def dispatch(self, request, *args, **kwargs):
        """dispatch

        """
        with open(STYLING_DEVELOPMENT_TEMPLATE, 'r') as file_handler:
            development_test_content = file_handler.read()
            development_test_content = development_test_content.replace('{{ SERVER_URL }}', SERVER_URL)
            development_test_content = development_test_content.replace('{{ APP }}', 'Mails')
            development_test_content = development_test_content.replace('{{ CATEGORY }}', 'development')
            development_test_content = development_test_content.replace('{{ TITLE }}', 'Licenses Server Development Test')

        send_mail(
            app='development',
            category='test',
            subject='Licenses Server Development Test',
            content=development_test_content,
            receivers=DEVELOPMENT_RECEIVERS,
            from_header='Licenses Server - SMTP development',
        )

        return HttpResponse('done')
