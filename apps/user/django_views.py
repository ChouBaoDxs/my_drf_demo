import logging

from django.views import View
from django.http import JsonResponse

logger = logging.getLogger('default')


def TestFBV(request, *args, **kwargs):
    logger.info('TestFBV')
    result = {
        'status': True,
        'data': 'response data'
    }
    if request.method == "GET":
        return JsonResponse(result)
    else:
        return JsonResponse(result)


class TestViewCBV(View):
    def get(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return JsonResponse(result)

    def post(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return JsonResponse(result)
