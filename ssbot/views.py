from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return HttpResponse("Index url")

@csrf_exempt
def botendpoint(request):
    if request.method=='POST':
            received_json_data=json.loads(request.body)
            #received_json_data=json.loads(request.body)
            return StreamingHttpResponse('POST received: ' + str(received_json_data))
    return StreamingHttpResponse('Accepting only POST')