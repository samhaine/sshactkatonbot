import os

from plugin_base.plugin import ApiAiBase, S_OK


class CompintelPlugin(ApiAiBase):
    def _read_token(self):
        return os.environ.get('COMPINTEL_PLUGIN')

    def company_knowledge(self):
        return self._ctx['speech'], S_OK
