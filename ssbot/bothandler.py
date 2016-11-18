import requests
import datetime
from sshackaton import settings

def getJWTtoken():
    """ Generates aut JWT token and returns, returns tuple (token, time stamp) """
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
    token = response.json()['access_token']
    return (token, datetime.datetime.now())


