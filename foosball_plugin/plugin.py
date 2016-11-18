import os

from plugin_base.plugin import ApiAiBase, S_OK


class FoosballPlugin(ApiAiBase):
    def _read_token(self):
        return os.environ.get('FOOSBALL_TOKEN')

    def user_wants_play(self):
        return self._ctx['speech'], S_OK
