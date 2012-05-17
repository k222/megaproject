# -*- coding: utf-8 -*-
import urllib, hashlib
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    last_activity =  DateTimeField()

    def get_gravatar_url(self):
        size = 100
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(size)})
        return gravatar_url

    def get_last_activity(self):
        if self.last_activity:
            delta = datetime.datetime.now() - self.last_activity
            if delta < datetime.timedelta(seconds=300):
                return "online"
            else:
                return "Последний раз был здесь: " + self.last_activity.strftime("%d.%m.%y, %H:%M")
        else:
            return "Последний раз был здесь: очень давно"

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def session_saved(sender, instance, created, **kwargs):
        id = instance.get_decoded().get('_auth_user_id')
        if id:
            user_profile = User.objects.get(pk=id).get_profile()
            user_profile.last_activity = datetime.datetime.now()
            user_profile.save()


    post_save.connect(create_user_profile, sender=User)
    post_save.connect(session_saved, sender=Session)

    @models.permalink
    def get_absolute_url(self):
        return ('profile', [str(self.user.username)])


class UserFriends(models.Model):
    user = models.ForeignKey(User, related_name='user_id')
    friends = models.ForeignKey(User, related_name='friends_id')