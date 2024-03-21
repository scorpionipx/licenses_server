from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)

from django.shortcuts import redirect

from django.template.loader import render_to_string

from django.views.generic import (
    TemplateView,
)

from django.urls import reverse, reverse_lazy


from licenses_server.mixins import (
    BaseMixin,
)


class HomePageView(BaseMixin, TemplateView):
    """HomePageView

    """
    # base mixin settings
    # ==================================================================================================================
    login_required = False
    # ==================================================================================================================

    template_name = 'home/core.html'
