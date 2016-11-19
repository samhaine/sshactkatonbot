import datetime
from sshackaton import settings
from django.http import HttpResponse
from ssbot.models import *
from django.utils import timezone
from datetime import *
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
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
    #TODO:Check refresh time of token (at  some blog it is stated liveTime is 30 mins and in other it is 60
    if timediff > timedelta(minutes=60):
        return False
    else:
        return True


def reply_skype_msg(message, conversation_id, recipient_name, replyToId):
    if is_token_valid():
        token = JWTRToken.objects.first()
        print "Token is Valid no need to update"
    else:
        print "Need to refresh token "
        getJWTtoken()
        token = JWTRToken.objects.first()

    headers = {
        'Authorization': 'Bearer ' + token.JWTtoken,
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {}
    data['type'] = 'message'
    data['timestamp'] = timezone.now().isoformat()
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
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    url = 'https://skype.botframework.com/v3/conversations/' + conversation_id + '/activities/' +replyToId
    r = requests.post(url, json_data, headers=headers)
    http_log_item = HTTPLoger(date=timezone.now(), httpStuff='POST status code: ' + str(r.status_code) + 'Req text: ' + str(r.text) + 'Content: ' + str(r.content))
    http_log_item.save()


def talkToALICE(input_msg):
    try:
        print input_msg
        if input_msg == 'joke':
            gross_joke = str(get_gross_joke().replace('<p>', '').replace('\n', '')).replace('<BLOCKQUOTE>', '').replace('</BLOCKQ', '')
            print gross_joke
            return gross_joke
        url = 'http://sheepridge.pandorabots.com/pandora/talk?botid=b69b8d517e345aba&skin=custom_input'
        data = {
            'botcust2': 'bdfc33b5de1b1c31',
            'input': input_msg
        }
        output_msg = requests.post(url, data=data).content
        return output_msg[output_msg.rfind("ALICE:")+7:]
    except:
        import traceback, sys
        traceback.print_exc(file=sys.stdout)


    return 'Sorry I am not myself today [internal server error or whateva... But I have joke for you ' + get_gross_joke().replace('<p>', '').replace('\n','')

def get_gross_joke():
    page = str(requests.post('http://www.randomjoke.com/topic/gross.php').text)
    joke = page[page.find('topic list"></P>\n<P>\n')+21:page.find('<CENTER>')-7]
    return str(joke.replace('<p>', ''))


def send_skype_msg(message, recipient_id, recipient_name):
    if recipient_id is None:
        print recipient_name.encode('UTF-8')
        recipient_id = UserIDs.objects.get(username__icontains = recipient_name.encode('UTF-8')).skypeid

    if is_token_valid():
        token = JWTRToken.objects.first()
        print "Token is Valid no need to update"
    else:
        print "Need to refresh token "
        getJWTtoken()
        token = JWTRToken.objects.first()

    headers = {
        'Authorization': 'Bearer ' + token.JWTtoken,
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {}
    data['type'] = 'message'
    data['timestamp'] = timezone.now().isoformat()
    data['from'] = {}
    data['from']['id'] = settings.BOT_RECIPIENT
    data['from']['name'] = settings.BOT_NAME
    data['conversation'] = {}
    data['conversation']['id'] = recipient_id
    data['recipient'] = {}
    data['recipient']['id'] = recipient_id
    data['recipient']['name'] = recipient_name
    data['text'] = message
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    url = 'https://skype.botframework.com/v3/conversations/' + recipient_id + '/activities/'
    r = requests.post(url, json_data, headers=headers)
    #http_log_item = HTTPLoger(date=timezone.now(), httpStuff='POST status code: ' + str(r.status_code) + 'Req text: ' + str(r.text) + 'Content: ' + str(r.content))
    #http_log_item.save()

def add_user_data(id, user_name):
    user, created = UserIDs.objects.get_or_create(skypeid=id, username = user_name)

