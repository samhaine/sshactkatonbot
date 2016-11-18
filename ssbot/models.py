from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HTTPLoger(models.Model):
    date = models.DateTimeField('date')
    httpStuff = models.TextField(blank=True, null=True)
