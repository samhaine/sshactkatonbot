import datetime, os

from plugin_base.plugin import ApiAiBase, S_OK

from .models import Approver, LinkPost

class AutofeedPlugin(ApiAiBase):
	def _read_token(self):
		return '398d090459b444699621cc4324ccf006' #this should not be here, but you know, fuck security because Hackaton

	def auto_feed(self):
		url = self._ctx['url']
		print "---------------------------------------------------------"
		print self._ctx['date']
		date = datetime.datetime.strptime(self._ctx['date'], '%Y-%m-%d')
		date = datetime.date(date.year, date.month, date.day)
		decisionmakers = self._ctx['any'].split('and') # this is the parameter's name in the api.ai, some problem?
		print url, date
		post = LinkPost.objects.create(link=url, post_date=date, approved=False)
		for dm in decisionmakers:
			apr = Approver.objects.create(name=dm, to_approve=post, approved=False)

		return self._ctx['speech'], S_OK

	def approve(self):
		user = self._ctx['name']
		links_ids = self._ctx['ids']

		# there is obvious race-condition here. Fortunately we won't run into it on the demo :P
		apprvs = Approver.objects().filter(name__exact=user, to_approve__in=links_ids)
		for app_record in apprvs:
			app_record.approved = True
			all_apprvs = app_record.to_approve.approver_set
			all_apprvs = [x.approved for x in all_apprvs]
			if all(all_apprvs):
				app_record.to_approve.approved = True
				app_record.to_approve.publish()
				app_record.to_approve.delete()
			else:
				app_record.save()

		return self._ctx['speech'], S_OK

	def deny(self):
		user = self._ctx['name']
		links_ids = self._ctx['ids']

		denied_posts = LinkPost.objects().filter(id__in=links_ids).delete()
		return self._ctx['speech'], S_OK

