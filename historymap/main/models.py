from django.db import models
from datetime import datetime

# Create your models here.
class Article(models.Model):
    url = models.URLField()
    title = models.TextField()
    times_generated = models.BigIntegerField(default = 0)
    times_searched = models.BigIntegerField(default = 0)
    times_hovered_over = models.BigIntegerField(default = 0)
    times_clicked_on = models.BigIntegerField(default = 0)
    date = models.BigIntegerField(default = 0)
    last_crawled = models.DateTimeField(null = True, blank = True)
    wikipedia_title_url = models.TextField(default = "")
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
