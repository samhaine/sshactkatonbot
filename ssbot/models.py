from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HTTPLoger(models.Model):
    date = models.DateTimeField('time stamp of post')
    httpStuff = models.TextField(blank=True, null=True)
