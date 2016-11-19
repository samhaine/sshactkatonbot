from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(unique=True, max_length=180)
    valid_to = models.DateTimeField()

    class Meta:
        ordering = ['valid_to']
