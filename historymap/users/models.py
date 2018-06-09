# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from datetime import datetime
import random

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

def get_new_deleted_user():
    return get_user_model().objects.get_or_create(username= "deleted"+ str(datetime.now()) + "rand" + str(random.randint(1,10000)))[0]

class UserArticle(models.Model):
    title = models.TextField()
    url = models.URLField()
    user = models.ForeignKey(User, on_delete = models.SET(get_new_deleted_user))
    times_hovered_over = models.BigIntegerField(default = 0)
    times_clicked_on = models.BigIntegerField(default = 0)
    times_searched = models.BigIntegerField(default = 0)
    wikipedia_title_url = models.TextField(default = "")
    last_visited = models.DateTimeField(default = datetime.now)
    first_visited = models.DateTimeField(default = datetime.now)
    
class UserYear(models.Model):
    year = models.IntegerField()
    times_requested = models.BigIntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.SET(get_new_deleted_user))
    first_visited = models.DateTimeField(default = datetime.now)
    last_visited = models.DateTimeField(default = datetime.now)

