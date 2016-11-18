from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
import os
import requests


def index(request):
    top_10_http_requests = HTTPLoger.objects.order_by('-date')[:10]
    output = ', '.join([http_request.httpStuff for http_request in top_10_http_requests])
    return HttpResponse(output)


@csrf_exempt
def botendpoint(request):
    if request.method=='POST':
            received_json_data=json.loads(request.body)
            #received_json_data=json.loads(request.body)
            return StreamingHttpResponse('POST received: ' + str(received_json_data))
    pass
    #return StreamingHttpResponse('Accepting only POST')


