from django.http import JsonResponse
from . import models
import json
from subscribers.serializers import SubscriberSerializer


def add(request):
    user, params = parse_request(request)
    if user is None:
        return get_error_response("user not found")

    result = user.add(params['money'])

    return get_response(user, result)


def subtract(request):
    user, params = parse_request(request)
    if user is None:
        return get_error_response("user not found")

    result = user.subtract(params['money'])

    return get_response(user, result)


def status(request):
    user, params = parse_request(request)
    if user is None:
        return get_error_response("user not found")

    return get_response(user, result=True)


def parse_request(request):
    json_body = json.loads(request.body.decode())
    params = json_body['addition']
    user = models.Subscriber.objects.filter(uuid=params['uuid']).first()

    return user, params


def get_response(user, result):
    response = {'result': result,
                'addition': SubscriberSerializer(user).data,
                'status': '200 OK'}

    return JsonResponse(response)


def get_error_response(error_text):
    response = {'result': False,
                'description': error_text,
                'status': '200 OK'}

    return JsonResponse(response)


def ping(request):
    return JsonResponse({'status': '200 OK'})
