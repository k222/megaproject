from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import  render_to_response
from achivki.main.views.login import mylogin

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    if request.user.is_authenticated():
        is_my_page = (user.username == request.user.username)

        context = {
            'is_my_page' : is_my_page,
            'is_authenticated' : True,
            'user_is_authenticated' : user.is_authenticated(),
            'username' : username,
            'gravatar_url' : user.get_profile().get_gravatar_url()
            #TODO: add feed content
        }

        return render_to_response("profile.html", context)
    else:
        return mylogin(request, redirect="/"+username)