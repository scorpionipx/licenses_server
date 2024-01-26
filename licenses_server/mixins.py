from django.conf import settings

from django.core.exceptions import PermissionDenied

from django.http import HttpResponseForbidden

from django.shortcuts import redirect, reverse

from django.utils.safestring import mark_safe


from licenses_server.responses import forbidden_response


class BaseMixin:
    """BaseMixin

        Base Mixin to be inherited by all Views.
    """
    PROJECT = settings.PROJECT
    VERSION = settings.VERSION

    THEME = settings.THEME

    login_required = True
    login_url = f'login/'

    groups_required = []
    admin_privileged = False

    forbidden_context = {}
    forbidden_template = ''

    def __init__(self, *args, **kwargs):
        """__init__

            Initialization.
        :param args: args
        :param kwargs: kwargs
        """
        if getattr(self, 'template_name', False):
            if getattr(self, 'THEME', False):
                if f'themes/{self.THEME}' in self.template_name:
                    pass  # only update template name if necessary
                else:
                    self.template_name = f'themes/{self.THEME}/{self.template_name}'  # noqa

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """get_context_data

            Custom context data.
        :param kwargs: kwargs
        :return: custom context data
        :rtype: dict
        """
        context = super(BaseMixin, self).get_context_data(**kwargs)  # noqa

        # server data
        # ==============================================================================================================
        context['SERVER'] = settings.SERVER
        context['VERSION'] = settings.VERSION
        # ==============================================================================================================

        # if self.request.user.is_authenticated:  # noqa
        #     if self.request.user.profile:  # noqa
        #         context['unread_notifications'] = self.request.user.profile.unread_notifications()  # noqa
        #         context['quick_notifications'] = self.request.user.profile.quick_notifications()  # noqa

        return context

    def dispatch(self, request, *args, **kwargs):
        """dispatch

            Custom dispatch.
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: custom dispatch
        """
        if self.login_required:
            if not request.user.is_authenticated:
                query = request.GET.urlencode()
                login_redirect_url = f'{reverse("login")}?next={request.path}'
                if query:
                    # if &, all query parameters will be stored as different elements within a QueryDict
                    # query is reformed at ved_hils_monitor/views.py LoginView.form_valid
                    query = query.replace('&', '~and~')
                    login_redirect_url = f'{login_redirect_url}?{mark_safe(query)}'

                return redirect(to=login_redirect_url)

        if self.groups_required:
            if self.admin_privileged and request.user.is_superuser:
                pass
            else:
                user_groups = [group.name for group in request.user.groups.all()]

                if not all(group in user_groups for group in self.groups_required):
                    if self.forbidden_context:
                        context = self.forbidden_context
                    else:
                        if len(self.groups_required) > 1:
                            groups_required_formatted = f'{", ".join(self.groups_required[:-1])} and ' \
                                                        f'{self.groups_required[-1]}'
                        else:
                            groups_required_formatted = f'{self.groups_required[0]}'
                        for group in self.groups_required:  # TODO: change this to better performance
                            groups_required_formatted = groups_required_formatted.replace(group, f'<b>{group}</b>')

                        context = {
                            'message': f'Access denied! You must be a member of {groups_required_formatted} '
                                       f'group{"s" if len(self.groups_required) > 1 else ""} in '
                                       f'order to access this page!'
                        }

                    if self.request.user.profile:  # noqa
                        context['unread_notifications'] = self.request.user.profile.unread_notifications()  # noqa
                        context['quick_notifications'] = self.request.user.profile.quick_notifications()  # noqa

                    # server data
                    # ==================================================================================================
                    context['SERVER'] = settings.SERVER
                    context['VERSION'] = settings.VERSION
                    # ==================================================================================================

                    template = self.forbidden_template

                    return forbidden_response(
                        context=context,
                        template=template,
                        request=request,
                    )

        return super(BaseMixin, self).dispatch(request, *args, **kwargs)
