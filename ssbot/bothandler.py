import datetime
from sshackaton import settings
from ssbot.models import *
from django.utils import timezone
from datetime import *
from django.utils import timezone
import json
from ssbot.models import *
import os
import requests


def getJWTtoken():
    """ Generates aut JWT token and returns, returns tuple (token, timestamp) """
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
    token = JWTRToken.objects.all()[:1].get().date
    token = JWTRToken(JWTtoken=response.json()['access_token'], date=timezone.now())
    token.save()
    return (token, datetime.datetime.now())


def is_token_valid():
    token_date = JWTRToken.objects.all()[:1].get().date
    timediff = timezone.now() - token_date
    if timediff > timedelta(minutes>59):
        return False
    else:
        return True

