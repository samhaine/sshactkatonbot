from __future__ import unicode_literals
import os
from django.db import models
import facebook

class Approver(models.Model):
	name = models.CharField(max_length=400)
	to_approve = models.ForeignKey('LinkPost')
	approved = models.BooleanField(default=False)

class LinkPost(models.Model):
	link = models.URLField()
	post_date = models.DateField()
	approved = models.BooleanField(default=False)

	def publish(self):
		APP_KEY = os.environ.get('FB_KEY')
		graph = facebook.GraphAPI(access_token=APP_KEY, version='2.2')
		att = {'name': '',
		    	'link': self.link,
			    'caption': '',
			    'description': '',
			    'picture': ''}
		graph.put_wall_post(message='', attachment=att)
