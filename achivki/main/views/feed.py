from django.http import Http404
from django.shortcuts import render_to_response
from achivki.main.models import UserProfile
from  achivki.main.views.login import mylogin

def feed(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(pk=request.user.id)
        context = {
            'user' : request.user,
            'gravatar_url' : user.get_gravatar_url()
        }
        return render_to_response("feed.html", context)
    else:
        return mylogin(request)
