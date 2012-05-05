import urllib, hashlib
from django.db import models
from django.contrib.auth.models import User
class UProfile(models.Model):
    name = models.CharField(max_length=75)
    password = models.CharField(max_length= 30)
    email = models.EmailField()

    def get_gravatar_url(self):
        default = "host664.hnt.ru/static/img/chuck.png"
        size = 100
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('profile', [str(self.id)])