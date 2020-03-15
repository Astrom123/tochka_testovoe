from django.http import JsonResponse
from . import models
import json
from subscribers.serializers import SubscriberSerializer


def add(request):
    user, params = parse_request(request)
    result = user.add(params['addition'])
    return get_response(user, result)


def subtract(request):
    user, params = parse_request(request)
    result = user.subtract(params['subtraction'])
    return get_response(user, result)


def status(request):
    user, params = parse_request(request)
    return get_response(user, result=True)


def parse_request(request):
    json_body = json.loads(request.body.decode())
    params = json_body['addition']
    user = models.Subscriber.objects.get(uuid=params['uuid'])
    return user, params


def get_response(user, result):
    response = {'result': result,
                'addition': SubscriberSerializer(user).data,
                'status': '200 OK'}
    return JsonResponse(response)


def ping(request):
    return JsonResponse({'status': '200 OK'})
