from django.conf import settings

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)


from django.views.generic import (
    View,
)

from mails.models import MailGroup


BASE_MODEL = MailGroup


SERVER_URL = settings.URL_BASE


class PlainReceiversView(View):
    """PlainReceiversView

    """
    def dispatch(self, request, *args, **kwargs):
        """dispatch

            Custom dispatch.
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: custom dispatch
        """
        try:
            mail_group = BASE_MODEL.objects.get(pk=self.kwargs['pk'])
            mail_group: MailGroup
        except BASE_MODEL.DoesNotExist:
            # noinspection PyProtectedMember
            content = f'Could not find any {BASE_MODEL._meta.verbose_name} matching pk: {self.kwargs["pk"]}'
            return HttpResponseBadRequest(content)

        content = ', '.join(mail_group.receivers)
        return HttpResponse(content)
