from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests

def getJWTtoken():
    AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    client_id = '73d727a4-6c40-4a72-a1a8-290f95ab7c64'
    client_secret = 'UQLaifGUroQnnnf1fO0hrct'
    payload = {
        'grant_type': "client_credentials",
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': "https://graph.microsoft.com/.default",
    }
    response = requests.post(AUTH_URL, data=payload)
    response.raise_for_status()
    token = response.json()['access_token']
    return token


