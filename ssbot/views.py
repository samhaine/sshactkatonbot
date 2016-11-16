from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import json


def index(request):
    return HttpResponse("Index url")


def botendpoint(request):
    if request.method=='POST':
            received_json_data=json.loads(request.body)
            #received_json_data=json.loads(request.body)
            return StreamingHttpResponse('POST received: ' + str(received_json_data))
    return StreamingHttpResponse('Accepting only POST')