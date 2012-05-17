
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import  render_to_response
from achivki.main.views.friends import  is_friend
import datetime

@login_required()
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404


    is_my_page = (user.username == request.user.username)
    user_profile = user.get_profile()

    print user_profile.last_activity
    context = {
        'is_my_page' : is_my_page,
        'is_authenticated' : True,
        'user_last_activity' : user_profile.get_last_activity(),
        'profile_name' : user.username,
        'my_username' : request.user.username,
        'gravatar_url' : user_profile.get_gravatar_url(),
        'already_friend':is_friend(request.user,user)
        #TODO: add feed content
    }

    return render_to_response("profile.html", context)