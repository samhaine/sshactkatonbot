import datetime
import os

from plugin_base.plugin import ApiAiBase, S_OK, S_INC
from foosball_plugin.models import User


class FoosballPlugin(ApiAiBase):

    def __init__(self, *args, **kwargs):
        super(FoosballPlugin, self).__init__(*args, **kwargs)

    def _read_token(self):
        return '520636da0efc44e582a4a960cc10f5be'

    def user_wants_play(self):
        now = datetime.datetime.now()
        valid_to = now + datetime.timedelta(minutes=15)
        user = User.objects.filter(name=self.user).first()
        if user is None:
            user = User.objects.create(name=self.user, valid_to=valid_to)
        else:
            user.valid_to = valid_to
            user.save()

        status = S_INC

        wanna_play = User.objects.filter(valid_to__gt=now).values_list('name', flat=True)[:2]
        if len(wanna_play) == 4:
            status = self.message_users(wanna_play, u'Users {} wanna play'.format(', '.join(wanna_play)))
            # self._ctx['speech'] = ''
            User.objects.filter(name__in=wanna_play).delete()

        return self._ctx['speech'], status
