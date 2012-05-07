from django.http import Http404
from django.shortcuts import render_to_response
from achivki.main.models import UserProfile
from  achivki.main.views.login import mylogin

def feed(request):
    if request.user.is_authenticated():
        context = {
            'username' : request.user.username,
            'gravatar_url' : request.user.get_profile().get_gravatar_url(),
            'is_authenticated' : True,
            # TODO: add feed content, sidebar content
        }
        return render_to_response("feed.html", context)
    else:
        return mylogin(request)
