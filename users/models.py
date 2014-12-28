from django.db import models

class Token(models.Model):
    name = models.CharField(max_length=64)
    token = models.CharField(max_length=64)
