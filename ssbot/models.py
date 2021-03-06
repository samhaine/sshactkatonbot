from __future__ import unicode_literals

from django.db import models


# Create your models here.
class HTTPLoger(models.Model):
    date = models.DateTimeField('date')
    httpStuff = models.TextField(blank=True, null=True)


class JWTRToken(models.Model):
    date = models.DateTimeField('date')
    JWTtoken = models.TextField(blank=True, null=True)


class UserIDs(models.Model):
    skypeid = models.CharField(max_length=100, unique=True)
    username = models.TextField()