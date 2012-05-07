import urllib, hashlib
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #name = models.CharField(max_length=75)                             --- use user.username instead
    #password = models.CharField(max_length= 30)                        --- WTF?! xDD
    #email = models.EmailField()                                        --- use user.email instead

    def get_gravatar_url(self):
        size = 100
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(size)})
        return gravatar_url

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    @models.permalink
    def get_absolute_url(self):
        return ('profile', [str(self.user.username)])