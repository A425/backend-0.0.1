from django.db import models
from django.utils import timezone

# 0 find things
# 1 find people

class Article(models.Model):
    intention = models.IntegerField()
    uid = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    cellphone = models.CharField(max_length=64)
    title = models.TextField()
    content = models.TextField()
    timestamp = models.FloatField()
