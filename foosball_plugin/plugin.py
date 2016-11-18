import json
import os

import apiai


API_TOKEN = os.environ.get('FOOSBALL_TOKEN')
ai = apiai.ApiAI(API_TOKEN)

S_FAIL = 'fail'
S_OK = 'ok'
S_INC = 'incapable'


class IncapableError(Exception):
    "Raise if the plugin can't handle given input"


def recognize(message):
    '''Connect with api.ai and return recognized action'''

    request = ai.text_request()
    request.query = message
    response = request.getresponse()
    if response.status != 200:
        raise IncapableError

    data = json.loads(response.read())
    try:
        action = globals().get(data['result']['action'], unknown_action)
        context = data['result']['parameters']
        context['speech'] = data['result']['fulfillment']['speech']
        return action, context
    except KeyError:
        raise IncapableError



def unknown_action(context):
    return '', S_INC


def user_wants_play(context):
    return context['speech'], S_OK
