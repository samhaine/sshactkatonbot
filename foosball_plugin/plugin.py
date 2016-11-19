import datetime
import os

from plugin_base.plugin import ApiAiBase, S_OK, S_NOT_DONE
from foosball_plugin.models import User


class FoosballPlugin(ApiAiBase):

    def __init__(self, *args, **kwargs):
        super(self, FoosballPlugin).__init__(*args, **kwargs)

    def _read_token(self):
        return os.environ.get('FOOSBALL_TOKEN')

    def user_wants_play(self):
        user, created = User.objects.get_or_create(name=self.user)
        now = datetime.datetime.now()
        user.valid_to = now + datetime.timedelta(minutes=15)
        user.save()
        status = S_NOT_DONE

        wanna_play = User.objects.filter(valid_to__gt=now).values_list('name', flat=True)[:4]
        if len(wanna_play) == 4:
            self.message_users(wanna_play, 'Users {} wanna play'.format(', '.join(wanna_play)))
            self._ctx['speech'] = ''
            User.objects.filter(name__in=wanna_play).delete()
            status = S_OK

        return self._ctx['speech'], status
