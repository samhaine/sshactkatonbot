from __future__ import unicode_literals

from django.db import models

class Approver(models.Model):
	name = models.CharField()
	to_approve = models.ForeignKey('LinkPost', on_delete=models.CASCADE)

class LinkPost(models.Model):
	link = models.URLField()
	post_date = models.DateField()
	approved = models.BooleanField(default=True)
