import json

from django.http import JsonResponse

from .plugin import S_INC, S_FAIL, recognize, IncapableError


def handle_message(request):
    payload = json.loads(request.body or '{}')
    out_data = {
        'response': '',
        'status': S_FAIL,
    }

    try:
        action, context = recognize(payload.get('message', 'I want to play foosball at 4 PM'))
        response, status = action(context)
        out_data['response'] = response
        out_data['status'] = status
    except IncapableError:
        out_data['status'] = S_INC
    except Exception as e:
        out_data['status'] = S_FAIL

    return JsonResponse(out_data)
