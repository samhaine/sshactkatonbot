from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.shortcuts import render
from django.utils import timezone
import json
from ssbot.models import *
from ssbot import bothandler
import os
import requests


def index(request):
    top_10_http_requests = HTTPLoger.objects.order_by('-date')[:10]
    template = loader.get_template('index.html')
    context = {
        'top_10_http_requests': top_10_http_requests,
    }
    return render(request, 'index.html', context)


@csrf_exempt
def botendpoint(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        #received_json_data=json.loads(request.body)##
        http_log_item = HTTPLoger(date=timezone.now(), httpStuff=str(request.META) + " \n JSON POST DATA: " +  str(received_json_data))
        http_log_item.save()
        #return StreamingHttpResponse('POST received: ' + str(received_json_data))
        return HttpResponse("asdfgfdsa")
    else:
        http_log_item = HTTPLoger(date=timezone.now(), httpStuff=str(request.META))
        http_log_item.save()
        return HttpResponse(str(request.META))

def refresh_token(request):
    bothandler.getJWTtoken()
    return HttpResponse(str('done'))
    ##bothandler.is_token_valid()
