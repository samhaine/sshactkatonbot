import datetime
from sshackaton import settings
from django.http import HttpResponse
from ssbot.models import *
from django.utils import timezone
from datetime import *
from django.utils import timezone
import json
from ssbot.models import *
import os
import requests


def getJWTtoken():
    """ Generates auth JWT token and returns, returns tuple (token, timestamp) """
    url = settings.AUTH_URL
    id = settings.BOT_ID
    passwd = settings.BOT_PASSWD
    payload = {
        'grant_type': "client_credentials",
        'client_id': id,
        'client_secret': passwd,
        'scope': "https://graph.microsoft.com/.default",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    token = JWTRToken.objects.first()
    token.JWTtoken = response.json()['access_token']
    token.date = timezone.now()
    token.save()
    return HttpResponse(token)


def is_token_valid():
    token_date = JWTRToken.objects.first()
    timediff = timezone.now() - token_date.date
    #TODO:  Check  refresh time of token (at  some blog it is stated liveTime is 30 mins and in other it is 60
    if timediff > timedelta(minutes=60):
        return False
    else:
        return True


def reply_skype_msg(message, conversation_id, recipient_name, replyToId):
    if is_token_valid():
        token = JWTRToken.objects.first()
    else:
        #getJWTtoken()
        token = JWTRToken.objects.first()

    headers = {
        'Authorization': 'Bearer ' + token.JWTtoken,
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {}
    data['type'] = 'message'
    data['timestamp'] = timezone.now()
    data['from'] = {}
    data['from']['id'] = settings.BOT_RECIPIENT
    data['from']['name'] = settings.BOT_NAME
    data['conversation'] = {}
    data['conversation']['id'] = conversation_id
    data['recipient'] = {}
    data['recipient']['id'] = conversation_id
    data['recipient']['name'] = recipient_name
    data['text'] = message
    data['replyToId'] = replyToId
    json_data = json.dump(data)
    url = 'https://skype.botframework.com/v3/conversations/' + conversation_id + '/activities/' +replyToId
    r = requests.post(url, json_data, headers=headers)
    http_log_item = HTTPLoger(date=timezone.now(), httpStuff="POST response: " + str(r))
    http_log_item.save()



