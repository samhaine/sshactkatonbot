import os

from plugin_base.plugin import ApiAiBase, S_OK


knowledge = {
    'google': ''' Google is owned by a Alphabet Inc.

        It hires over 61 thousand people. It's main site is http://google.com''',
    'facebook': ''' Facebook is a social media website.

        There are over 1 bilion users registered.''',
    'apple': '''Apple is a manufacturer of overpriced electronic devices.

        iPhone is great, anyway.''',
    'twitter': '''
        ''',
    'instagram': '''A place for sharing photos.

        Owned by Facebook.''',
    'softserve': '''Well, this is a company you are working in.
        ''',
    'zenoss': '''Enterprise monitoring platform.

        Dude, it's big.''',
    'attainia': '''Facility to help you build a hostpital.

        Big database of medical devices.''',
}


class CompintelPlugin(ApiAiBase):
    def _read_token(self):
        return os.environ.get('COMPINTEL_PLUGIN')

    def company_knowledge(self):
        company = self._ctx.get('Company', '').lower()
        data = knowledge.get(company, '')
        if data:
            self._ctx['speech'] = data
        return self._ctx['speech'], S_OK
