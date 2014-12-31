from django.db import models
from django.utils import timezone

# 1 find something
# 2 find some people
class Article(models.Model):
    intention = models.IntegerField()
    name = models.CharField(max_length=64)
    cellphone = models.CharField(max_length=64)
    title = models.TextField()
    content = models.TextField()
    createDate = models.DateTimeField(default=timezone.now)
