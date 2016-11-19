import datetime, os

from plugin_base.plugin import ApiAiBase, S_OK

from .models import Approver, LinkPost

class AutofeedPlugin(ApiAiBase):
    def _read_token(self):
        return os.environ.get('AUTOFEED_TOKEN')

    def auto_feed(self):
        return self._ctx['speech'], S_OK

    def decisionmakers(self):
    	url = self._ctx['url']
    	date = datetime.datetime.strptime(self._ctx['date'], 'mm-dd-yyyy')
    	date = datetime.date(date.year, date.month, date.day)
    	decisionmakers = self._ctx['any'].split('and') # this is the parameter's name in the api.ai, some problem?

    	post = LinkPost(url, date, false)
    	post.save()
    	for dm in decisionmakers:
    		apr = Approver(dm, post)
    		apr.save()

    	return self._ctx['speech'], S_OK

    def approve(self):
    	pass

    def deny(self):
    	pass
