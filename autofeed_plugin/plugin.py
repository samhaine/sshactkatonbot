import os

from plugin_base.plugin import ApiAiBase, S_OK


class AutofeedPlugin(ApiAiBase):
    def _read_token(self):
        return os.environ.get('AUTOFEED_TOKEN')

    def auto_feed(self):
        return self._ctx['speech'], S_OK

    def decisionmakers(self):
    	return None, S_OK