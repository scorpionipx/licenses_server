import json


from django.http import (
    HttpResponse,
    JsonResponse,
)


from django.views import (
    View,
)


from licenses.models import License

from licenses_server.mixins import BaseMixin


BASE_MODEL = License


class AsJSONView(View):
    """
    AsJSONView
    """
    for_humans = False

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch
        """
        try:
            entry = BASE_MODEL.objects.get(pk=self.kwargs['pk'])
        except BASE_MODEL.DoesNotExist as exception:
            data = {
                'error': f'{exception}'
            }
            return JsonResponse(data)
        except Exception as exception:
            data = {
                'error': f'{exception}'
            }
            return JsonResponse(data)

        if self.for_humans:
            data = entry.as_json()
            response = f'<pre>{data}</pre>'
            return HttpResponse(response)
        else:
            data = entry.as_dict()
            return JsonResponse(data)


class AsJSONForHumansView(AsJSONView):
    """
    AsJSONForHumansView
    """
    for_humans = True
