import json

import apiai
import requests
from django.http import JsonResponse


S_FAIL = 'fail'
S_OK = 'ok'
S_NOT_DONE = 'not-done'
S_INC = 'incapable'


class IncapableError(Exception):
    "Raise if the plugin can't handle given input"


class ApiAiBase(object):
    BOT_URL = 'http://example.org'  # FIXME obviusly wrong address

    def __init__(self, user, ctx):
        self.user = user
        self._ctx = ctx
        self.action = self.unknown_action
        self._ai = apiai.ApiAI(self._read_token())

    def _read_token(self):
        raise NotImplementedError("Subclasses should implement this!")

    def recognize(self, message):
        request = self._ai.text_request()
        request.query = message
        response = request.getresponse()
        if response.status != 200:
            raise IncapableError

        data = json.loads(response.read())
        try:
            self.action = getattr(self, data['result']['action'], self.unknown_action)
            self._ctx.update(data['result']['parameters'])
            self._ctx['speech'] = data['result']['fulfillment']['speech']
        except KeyError:
            raise IncapableError

    def message_user(self, users, message):
        data = {
            'users': users,
            'message': message,
        }
        resp = requests.get(self.BOT_URL, data)
        status = S_FAIL
        if resp.status_code == 200:
            status = S_OK
        return status

    def unknown_action(self):
        return '', S_INC


def get_handler(pluginClass):

    def handle_message(request):
        payload = json.loads(request.body or '{}')
        out_data = {
            'response': '',
            'status': S_FAIL,
        }

        try:
            plugin = pluginClass(
                payload.get('user', None),
                payload.get('context', {}),
            )
            plugin.recognize(payload.get('message', ''))
            response, status = plugin.action()
            out_data['response'] = response
            out_data['status'] = status
        except IncapableError:
            out_data['status'] = S_INC

        return JsonResponse(out_data)

    return handle_message
