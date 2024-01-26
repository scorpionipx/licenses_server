import json


from django.http import (
    HttpResponseBadRequest,
    HttpResponse,
    JsonResponse,
)

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.views import (
    View,
)


from licenses.models import License

from licenses.model_based_utils.license import Cryptor

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


@method_decorator(csrf_exempt, name='dispatch')
class GetView(View):
    """
    GetView
    """
    @staticmethod
    def post(request):
        """

        """
        cryptor = Cryptor()

        try:
            payload = json.loads(cryptor.decrypt(request.body.decode('utf-8')))
        except Exception as exception:
            error = f'Failed to read request: {exception}'
            return HttpResponseBadRequest(error)

        aes_key = payload.get('AESKey', None)
        if not aes_key:
            error = 'No AES key specified!'
            return HttpResponseBadRequest(error)

        init_vector = payload.get('InitVector', None)
        if not init_vector:
            error = 'No InitVector specified!'
            return HttpResponseBadRequest(error)

        serial_no = payload.get('SerialNo', None)
        if not serial_no:
            error = 'No SerialNo specified!'
            return HttpResponseBadRequest(error)

        try:
            entry = License.objects.get(serial_no=serial_no)
            entry: License
        except License.DoesNotExist as exception:
            error = f'Failed to find matching License: {exception}'
            return HttpResponseBadRequest(error)

        entry_data = json.dumps(entry.as_dict(serializable=True), indent=2)

        response = cryptor.encrypt(
            plain_text=entry_data.encode('utf-8'),
            aes_key=bytes.fromhex(aes_key),
            init_vector=bytes.fromhex(init_vector),
        )

        return HttpResponse(response)
