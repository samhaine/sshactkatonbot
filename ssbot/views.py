from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.shortcuts import render
from django.utils import timezone
import json
from ssbot.models import *
from ssbot import bothandler
from plugin_base.plugin import IncapableError, S_FAIL, S_OK
from autofeed_plugin.plugin import *
from  compintel_plugin.plugin import *
from foosball_plugin.plugin import *

import os
import requests

def autodiscovery(username, message):
    username =  username.encode('utf-8')
    for p in [CompintelPlugin(username, {}), FoosballPlugin(username, {}), AutofeedPlugin(username, {})]:
        try:

            p.recognize(message)
            return p.action()
        except IncapableError:
            pass
        # except Exception as e:
        #     print e
    return message, S_FAIL


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
        http_log_item = HTTPLoger(date=timezone.now(), httpStuff=str(request.META) + " \n JSON POST  DATA: " +  str(received_json_data))
        http_log_item.save()
        if received_json_data['type'] == 'message':
            msg, status = autodiscovery(received_json_data['from']['name'], received_json_data['text'])
            if msg  :
                bothandler.reply_skype_msg(
                    msg,
                    received_json_data['conversation']['id'],
                    received_json_data['from']['name'],
                    received_json_data['id']
                )
                return StreamingHttpResponse('POST apiai')
            else:
                get_AI_reply_from_ALICE_bot = bothandler.talkToALICE(received_json_data['text'])
                bothandler.reply_skype_msg(
                    get_AI_reply_from_ALICE_bot,
                    received_json_data['conversation']['id'],
                    received_json_data['from']['name'],
                    received_json_data['id']
                )
                return StreamingHttpResponse('POST chatbot')
        elif received_json_data['type'] == 'add' or received_json_data['type']=='contactRelationUpdate':
            bothandler.add_user_data(received_json_data['from']['id'], received_json_data['from']['name'])
            return StreamingHttpResponse('Contact exchanged')
        else:
            return StreamingHttpResponse('POST received: ' + str(received_json_data))

    else:
        bothandler.send_skype_msg("COMM: BOT -> USER", '29:1psxojXwFAB0yv7pz-Z1DynvRQwxO2ffxh5Lwo7oZoAJEfu_nBYq7UdIKMcC0X9fN', 'Rados\u0142aw Warzocha')
        http_log_item = HTTPLoger(date=timezone.now(), httpStuff=str(request.META))
        http_log_item.save()
        return HttpResponse(str(request.META))

def refresh_token(request):
    bothandler.getJWTtoken()
    return HttpResponse(str('done'))
    ## bothandler.is_token_valid()

@csrf_exempt
def voice_chanel(request):
    http_log_item = HTTPLoger(date=timezone.now(), httpStuff=str(request.META))
    http_log_item.save()
    msg = request.META['HTTP_MESSAGEFROMDIMA']
    get_AI_reply_from_ALICE_bot = bothandler.talkToALICE(msg)
    return HttpResponse(get_AI_reply_from_ALICE_bot)



