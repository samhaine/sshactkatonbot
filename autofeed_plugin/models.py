from __future__ import unicode_literals

from django.db import models

class Approver(models.Model):
	name = models.CharField(max_length=400)
	to_approve = models.ForeignKey('LinkPost')
	approved = models.BooleanField(default=False)

class LinkPost(models.Model):
	link = models.URLField()
	post_date = models.DateField()
	approved = models.BooleanField(default=False)
